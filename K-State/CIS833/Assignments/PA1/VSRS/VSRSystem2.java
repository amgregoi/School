import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.StringReader;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.stream.StreamSource;

import org.apache.commons.io.FileUtils;
import org.apache.commons.lang.SerializationUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.serializer.Serializer;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

import edu.umd.cloud9.util.Histogram;
import edu.umd.cloud9.util.MapKI.Entry;
import edu.umd.cloud9.io.ArrayListWritable;
import edu.umd.cloud9.io.PairOfFloatInt;
import edu.umd.cloud9.io.PairOfInts;
import edu.umd.cloud9.io.PairOfStringFloat;
import edu.umd.cloud9.io.PairOfStrings;

public class VSRSystem2 {

	// inverted index mapper
	// Cloud9 structures
	// Borrwed Histogram - to get term frequency in document
	// Borrow PairOfInts - to return value (doc_id, tf)
	public static class BuildInvertedIndex extends
			Mapper<Object, Text, Text, PairOfStrings> {

		private Text word = new Text();
		private HashMap<String, String> stopWord;
		private Stemmer stem;
		private Histogram<String> termCounts = new Histogram<String>();
		private float maxTF;

		@Override
		public void setup(Context context) {
			Configuration conf = context.getConfiguration();
			String filename = conf.get("stopwords");

			/* Initialize stop word hash map and stemmer */
			stopWord = new HashMap<String, String>();
			stem = new Stemmer();
			try {
				/* Builds the stop word hash map */
				FileReader file = new FileReader(filename);
				BufferedReader bf = new BufferedReader(file);
				String line;
				while ((line = bf.readLine()) != null) {
					stopWord.put(line, line);
				}
				bf.close();
			} catch (Exception e) {
			}
		}

		public void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {
			String docNum = null;
			termCounts.clear();
			maxTF = 0;
			// gets the required parts of the document, excluding tags
			final Pattern doc = Pattern.compile("(.+?)<DOC>");
			final Pattern title = Pattern.compile("<TITLE>(.+?)</TITLE>");
			final Pattern text = Pattern.compile("<TEXT>(.+?)</TEXT>");

			final Matcher matcher1 = title.matcher(value.toString());
			final Matcher matcher2 = text.matcher(value.toString());
			final Matcher matcher3 = doc.matcher(value.toString());
			matcher1.find();
			matcher2.find();
			matcher3.find();
			String s = matcher3.group(1) + " " + matcher1.group(1) + " "
					+ matcher2.group(1);

			// tokenizer for the returned parts of the corpus
			StringTokenizer itr = new StringTokenizer(s.toLowerCase(),
					" \t\n\r\f,.:;?![]'!@#$%^&*()_+-=\\/");

			// Iterates through the tokenizer and adds to histogram for the
			// wordcount
			while (itr.hasMoreTokens()) {
				String term = itr.nextToken();
				if (term.contains("cranfield") && !term.equals("cranfield")) {
					docNum = term.replace("cranfield", "");
				}
				if (term == null || term.length() == 0)
					continue;
				/* Checks if token is numeric and against the stop word hashmap */
				if (term.matches("-?\\d+(\\.\\d+)?")
						|| stopWord.containsKey(term)) {
					continue;
				}

				stem.add(term.toCharArray(), term.length());
				stem.stem();
				String w = stem.toString();
				termCounts.count(w + "," + docNum);
			}

			for (Entry<String> e : termCounts.entrySet()) {
				if (e.getValue() > maxTF)
					maxTF = e.getValue();
			}

			// Iterates through histogram and emits the key value pair (word,
			// <document_id, count of word from histogram>)
			for (Entry<String> e : termCounts.entrySet()) {
				String w = e.getKey();
				int comma = w.indexOf(",");
				String docNumber = w.substring(comma + 1, w.length());
				BigDecimal bd = new BigDecimal(e.getValue() / maxTF).setScale(
						4, RoundingMode.HALF_UP);
				word.set(w.substring(0, comma));
				context.write(word,
						new PairOfStrings(docNumber, bd.toPlainString()));
			}

		}
	}

	// Inverted index reducer
	// Cloud9 structures
	// Borrowed ArrayListWritable to create a list of PairOfInt objects for our
	// inverted index
	// the above is also our value returned for the reducer
	private static class reduceInvertedIndex
			extends
			// Reducer<Text, PairOfInts, Text, InvertedIndexObject> { // new
			Reducer<Text, PairOfStrings, PairOfStrings, ArrayListWritable<PairOfStrings>> { // original

		public void reduce(Text key, Iterable<PairOfStrings> values,
				Context context) throws IOException, InterruptedException {
			ArrayListWritable<PairOfStrings> postings = new ArrayListWritable<PairOfStrings>();
			int count = 0;
			// adds PairOfInts to arraylist postings
			for (PairOfStrings poi : values) {
				postings.add(poi.clone());
				count++;
			}
			// emits inverted index row
			context.write(
					new PairOfStrings(key.toString(), Integer.toString(count)),
					postings);
		}
	}

	// Calculates document count
	// mapper
	private static class DocLengthMap extends
			Mapper<Object, Text, Text, InvertedIndexObject> {

		InvertedIndexObject iio;

		public void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {
			StringTokenizer st = new StringTokenizer(value.toString(),
					" \t\n\r\f,:;?![]'!@#$%^&*()_+-=\\/");

			String s = st.nextToken();
			int df = Integer.parseInt(st.nextToken());
			iio = new InvertedIndexObject(s, df);
			while (st.hasMoreElements()) {
				String docNum = st.nextToken();
				BigDecimal tf = new BigDecimal(st.nextToken());
				iio.addToIndex(new PairOfStringFloat(docNum, tf.floatValue()));
			}
			context.write(new Text(""), iio);
		}
	}

	// Calculates document count
	// reducer
	private static class DocLengthReduce extends
			Reducer<Text, InvertedIndexObject, Text, Text> {
		public void reduce(Text key, Iterable<InvertedIndexObject> values,
				Context context) throws IOException, InterruptedException {
			HashMap<String, Integer> documents = new HashMap<>();
			// Calculates document count
			Iterator i = values.iterator();
			while (i.hasNext()) {
				InvertedIndexObject iio = (InvertedIndexObject) i.next();
				for (PairOfStringFloat index : iio.getIndex()) {
					if (!documents.containsKey(index.getLeftElement())) {
						documents.put(index.getLeftElement(), 1);
					}
				}
				// System.out.println(iio.getWord());
			}
			context.write(new Text(Integer.toString(documents.size())),
					new Text(""));
		}
	}

	//
	// job3mapper finds document length
	private static class job3Mapper extends
			Mapper<Object, Text, Text, FloatWritable> {

		InvertedIndexObject iio;
		int docCount;

		@Override
		public void setup(Context context) {
			Configuration conf = context.getConfiguration();
			String filename = conf.get("docCount");
			docCount = 0;
			try {
				FileReader file = new FileReader(filename);
				BufferedReader bf = new BufferedReader(file);
				StringTokenizer st = new StringTokenizer(bf.readLine());
				docCount = Integer.parseInt(st.nextToken());
				bf.close();
			} catch (Exception e) {
				System.out.println("Exception: " + e.toString());
				System.exit(-1);
			}
		}

		public void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {
			StringTokenizer st = new StringTokenizer(value.toString(),
					" \t\n\r\f,:;?![]'!@#$%^&*()_+-=\\/");

			String s = st.nextToken();
			int df = Integer.parseInt(st.nextToken());
			iio = new InvertedIndexObject(s, df);
			while (st.hasMoreElements()) {
				String docNum = st.nextToken();
				BigDecimal tf = new BigDecimal(st.nextToken());
				BigDecimal num = new BigDecimal(Math.log(docCount
						/ iio.getDF().get()));
				BigDecimal denom = new BigDecimal(Math.log(2)).setScale(4,
						RoundingMode.HALF_UP);
				BigDecimal idf = new BigDecimal(num.floatValue()
						/ denom.doubleValue())
						.setScale(4, RoundingMode.HALF_UP);
				BigDecimal tf_idf = new BigDecimal(idf.floatValue()
						* tf.floatValue()).setScale(4, RoundingMode.HALF_UP);
				iio.addToIndex(new PairOfStringFloat(docNum, tf_idf
						.floatValue()));
			}

			for (PairOfStringFloat p : iio.getIndex()) {
				String doc = p.getLeftElement();
				float val = p.getRightElement();

				context.write(new Text(doc), new FloatWritable(val));
			}

			// context.write(new Text(s), new FloatWritable();
		}
	}

	//
	// job3reducer finds document length
	private static class job3Reducer extends
			Reducer<Text, FloatWritable, Text, FloatWritable> {

		public void reduce(Text key, Iterable<FloatWritable> values,
				Context context) throws IOException, InterruptedException {
			// adds PairOfInts to arraylist postings
			float sumTFIDF = 0;
			for (FloatWritable f : values) {
				sumTFIDF += Math.pow(f.get(), 2);

			}
			BigDecimal length = new BigDecimal(Math.sqrt(sumTFIDF)).setScale(4,
					RoundingMode.HALF_UP);
			context.write(key, new FloatWritable(length.floatValue()));
		}
	}

	//
	// job4mapper, builds final index (with tf-idf)
	private static class job4Mapper extends
			Mapper<Object, Text, Text, PairOfStrings> {

		InvertedIndexObject iio;
		int docCount;

		@Override
		public void setup(Context context) {
			Configuration conf = context.getConfiguration();
			String filename = conf.get("docCount");
			docCount = 0;
			try {
				FileReader file = new FileReader(filename);
				BufferedReader bf = new BufferedReader(file);
				StringTokenizer st = new StringTokenizer(bf.readLine());
				docCount = Integer.parseInt(st.nextToken());
				bf.close();
			} catch (Exception e) {
				System.out.println("Exception: " + e.toString());
			}
		}

		public void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {
			StringTokenizer st = new StringTokenizer(value.toString(),
					" \t\n\r\f,:;?![]'!@#$%^&*()_+-=\\/");

			String s = st.nextToken();
			int df = Integer.parseInt(st.nextToken());
			iio = new InvertedIndexObject(s, df);
			while (st.hasMoreElements()) {
				String docNum = st.nextToken();
				BigDecimal tf = new BigDecimal(st.nextToken());
				BigDecimal tf_idf = new BigDecimal(tf.floatValue()
						* (Math.log(docCount / (double) iio.getDF().get()))
						/ Math.log(2)).setScale(4, RoundingMode.HALF_UP);
				iio.addToIndex(new PairOfStringFloat(docNum, tf_idf
						.floatValue()));

				context.write(new Text(s),
						new PairOfStrings(docNum, tf_idf.toPlainString()));
			}

		}
	}

	//
	// Main function
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf, args)
				.getRemainingArgs();
		if (otherArgs.length < 3) {
			System.err
					.println("Usage: wordcount <in> [<in>...] <out> <stopword_list>");
			System.exit(2);
		}
		FileSystem.get(conf).delete(new Path(otherArgs[1]), true);
		FileSystem.get(conf)
				.delete(new Path(otherArgs[1] + "_doc_count"), true);
		FileSystem.get(conf).delete(new Path(otherArgs[1] + "_doc_length"),
				true);
		FileSystem.get(conf).delete(new Path(otherArgs[1] + "_final_index"),
				true);

		if (doJob1(otherArgs, conf)) {
			// DO NEXT JOB
			if (doJob2(otherArgs, conf)) {
				if (doJob3(otherArgs, conf))
					if (doJob4(otherArgs, conf)) {
						new QueryAnswer().query(otherArgs[1]
								+ "_final_index/part-r-00000", otherArgs[1]
								+ "_doc_count/part-r-00000", otherArgs[1]
								+ "_doc_length/part-r-00000");
						System.exit(0);
					}
			}
		}
	}

	
	// Job 1 pre processes our corpus Eliminates SGML tags Tokenizes on spaces
	// and punction stems words filters out stop words and numbers
	public static boolean doJob1(String[] otherArgs, Configuration conf)
			throws Exception {
		conf.set("stopwords", otherArgs[2]);// stop word path
		Job job = Job.getInstance(conf);
		job.setJarByClass(VSRSystem2.class);
		job.setMapperClass(BuildInvertedIndex.class);
		job.setReducerClass(reduceInvertedIndex.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(PairOfStrings.class); // original

		for (int i = 0; i < otherArgs.length - 2; ++i) {
			FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
		}
		FileOutputFormat.setOutputPath(job, new Path(
				otherArgs[otherArgs.length - 2]));
		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}

	//
	// finds total document count
	public static boolean doJob2(String[] otherArgs, Configuration conf)
			throws Exception {
		conf.set("docLength", otherArgs[1]); // output path
		Job job = Job.getInstance(conf);
		job.setJarByClass(VSRSystem2.class);
		job.setMapperClass(DocLengthMap.class);
		job.setReducerClass(DocLengthReduce.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(InvertedIndexObject.class);
		for (int i = 1; i < otherArgs.length - 1; ++i) {
			FileInputFormat.addInputPath(job, new Path(otherArgs[i]
					+ "/part-r-00000"));
		}
		FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]
				+ "_doc_count"));
		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}

	//
	// calculates document length
	public static boolean doJob3(String[] otherArgs, Configuration conf)
			throws Exception {
		conf.set("docCount", otherArgs[1] + "_doc_count/part-r-00000");// stop
																		// word
																		// path
		Job job = Job.getInstance(conf);
		job.setJarByClass(VSRSystem2.class);
		job.setMapperClass(job3Mapper.class);
		job.setReducerClass(job3Reducer.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(FloatWritable.class);
		for (int i = 1; i < otherArgs.length - 1; ++i) {
			FileInputFormat.addInputPath(job, new Path(otherArgs[i]
					+ "/part-r-00000"));
		}
		FileOutputFormat.setOutputPath(job, new Path(
				otherArgs[otherArgs.length - 2] + "_doc_length"));
		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}

	//
	// builds final index
	public static boolean doJob4(String[] otherArgs, Configuration conf)
			throws Exception {
		conf.set("docCount", otherArgs[1] + "_doc_count/part-r-00000");// stop
																		// word
																		// path
		Job job = Job.getInstance(conf);
		job.setJarByClass(VSRSystem2.class);
		job.setMapperClass(job4Mapper.class);
		job.setReducerClass(reduceInvertedIndex.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(PairOfStrings.class);
		for (int i = 1; i < otherArgs.length - 1; ++i) {
			FileInputFormat.addInputPath(job, new Path(otherArgs[i]
					+ "/part-r-00000"));
		}
		FileOutputFormat.setOutputPath(job, new Path(
				otherArgs[otherArgs.length - 2] + "_final_index"));
		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}
}
