import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Partitioner;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import edu.umd.cloud9.io.PairOfStringInt;

public class PageRank {

	 /*
	 * Mapper for job 1
	 * Outputs a page and itself so pages with no outward links may be kept
	 * and also Outputs a page with links in that page
	 */
	private static class LinkGraphJ1Mapper extends Mapper<Object, Text, PairOfStringInt, Text> {
		private PairOfStringInt mKey = new PairOfStringInt();
		private Text mValue = new Text();

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
			String pageTitle = null;
			ArrayList<String> listOfLinks = new ArrayList<String>();

			final Pattern title = Pattern.compile("<title>(.+?)</title>");
			final Pattern text = Pattern.compile("<text>(.+?)</text>");
			final Pattern linkPattern = Pattern.compile("\\[\\[(.*?)\\]\\]");

			final Matcher titleMatcher = title.matcher(value.toString());
			final Matcher textMatcher = text.matcher(value.toString());
			final Matcher linkMatcher;

			if (titleMatcher.find() && !(pageTitle = titleMatcher.group(1)).contains(":")) {
				pageTitle = pageTitle.replace(" ", "_");
				mKey.set(pageTitle, 0);
				mValue.set(pageTitle);
				context.write(mKey, mValue);

				if (textMatcher.find()) {
					String linkTitles = textMatcher.group(1).replace(" ", "");
					linkMatcher = linkPattern.matcher(linkTitles);

					while (linkMatcher.find()) {
						String linkTitle = linkMatcher.group(1);
						if (!linkTitle.contains(":")) {
							if (linkTitle.contains("|")) {
								linkTitle = linkTitle.substring(0, linkTitle.indexOf("|"));
							} else if (linkTitle.contains("#")) {
								linkTitle = linkTitle.substring(0, linkTitle.indexOf("#"));
							}
							if (!listOfLinks.contains(linkTitle))
								listOfLinks.add(linkTitle);
						}
					}
				}

				for (String link : listOfLinks) {
					mKey.set(link, 1);
					mValue.set(pageTitle);
					context.write(mKey, mValue);
				}
			}
		}
	}

	 /*
	 * Reducer for job 1
	 * Outputs pairs of pages and links in that pages
	 */
	private static class LinkGraphJ1Reducer extends Reducer<PairOfStringInt, Text, Text, Text> {
		private String sCurrentPage = null;
		private Text wikiPage = new Text();

		public void reduce(PairOfStringInt key, Iterable<Text> values, Context context) throws IOException, InterruptedException {

			if (key.getRightElement() == 0) {
				wikiPage.set(key.getLeftElement());
				context.write(wikiPage, wikiPage);
				sCurrentPage = key.getLeftElement();
			}
			if (key.getRightElement() == 1 && key.getLeftElement().equals(sCurrentPage)) {
				for (Text links : values) {
					wikiPage.set(key.getLeftElement());
					context.write(links, wikiPage);
				}
			}
		}
	}

	/*
	* Mapper for job 1.5
	* Ouputs valid pageTitles in order to calculate the corpus size
	*/
	private static class CorpusSizeJ1_5Mapper extends Mapper<Object, Text, Text, Text> {
		private Text output = new Text("1");

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

			final Pattern title = Pattern.compile("<title>(.+?)</title>");
			final Matcher titleMatcher = title.matcher(value.toString());

			if (titleMatcher.find() && !titleMatcher.group(1).contains(":")) {
				context.write(output, output);
			}

		}
	}

	/*
	* Reducer for job 1.5
	* Outputs corpus size
	*/
	private static class CorpusSizeJ1_5Reducer extends Reducer<Text, Text, Text, IntWritable> {
		private Text blankKey = new Text();
		private IntWritable corpusSize = new IntWritable();

		public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {

			int count = 0;
			for (Text c : values) {
				count++;
			}
			corpusSize.set(count);
			context.write(blankKey, corpusSize);
		}
	}

	/*
	* Mapper for job 2
	* Outputs pageTitle and a link on that page or itself to created the
	* linked graph
	*/
	private static class LinkGraphJ2Mapper extends Mapper<Object, Text, Text, Text> {
		private Text wikiPage = new Text();
		private Text pageLink = new Text();

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
			String values[] = value.toString().split("\t");

			wikiPage.set(values[0]);
			pageLink.set(values[1]);
			context.write(wikiPage, pageLink);
		}
	}

	/*
	* Reducer for job 2
	* Outputs link graph which is the base of the pageRank
	*/
	private static class LinkGraphJ2Reducer extends Reducer<Text, Text, Text, Text> {
		private Text mKey = new Text();
		private Text adjacencyList = new Text();

		public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
			String adjacencyListValue = "";

			for (Text ref : values) {
				if (!ref.toString().equals(key.toString())) {
					adjacencyListValue += ("--" + ref);
				}
			}
			float initialPR = 1.0f/Float.parseFloat(context.getConfiguration().get("corpus_size"));

			mKey.set(key.toString());
			adjacencyList.set("--"+initialPR+"--"+initialPR+adjacencyListValue);
			context.write(mKey, adjacencyList);
		}
	}

	/*
	* Mapper for job 3
	*/
	public static class PageRankJ3Mapper extends Mapper<Object, Text, Text, PairOfStringInt> {
		private Text mKey = new Text();
		private PairOfStringInt mValue = new PairOfStringInt();

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
			ArrayList<String> outwardLinks = new ArrayList<String>();
			String values[] = value.toString().replaceAll("\\s", "").split("--");
			String pageTitle = values[0];
			String outwardLinkString = "--";
			float pageRank = Float.parseFloat(values[1]);
			
			for(int i = 3; i<values.length; i++){
				outwardLinks.add(values[i]);
				outwardLinkString += values[i]+"--";
			}
			if (!pageTitle.equals("")) {
				for (String link : outwardLinks) {
					mKey.set(link);
					mValue.set(Float.toString(pageRank / outwardLinks.size()), 0);
					context.write(mKey, mValue);
				}
				if (outwardLinks.size() == 0) {
					mKey.set(pageTitle);
					mValue.set("", 1);
					context.write(mKey, mValue);
				}else{
					mKey.set(pageTitle);
					mValue.set(outwardLinkString, 1);
					context.write(mKey, mValue);
				}
				mKey.set(pageTitle);
				mValue.set(Float.toString(pageRank), 2);
				context.write(mKey, mValue);
			}
		}
	}

	/*
	* Reducer for job 3
	* Calculates pageRank
	* Outputs row in the pageRank node list
	* of the format: "(pageTitle, pageRank)		--link1--link2--link3"
	*/
	private static class PageRankJ3Reducer extends Reducer<Text, PairOfStringInt, Text, Text> {
		private Text mKey = new Text();
		private Text mValue = new Text();

		public void reduce(Text key, Iterable<PairOfStringInt> values, Context context) throws IOException, InterruptedException {

			float newScore = 0;
			float oldScore = 0;
			float epsilon = Float.parseFloat(context.getConfiguration().get("epsilon"));
			int corpusSize = Integer.parseInt(context.getConfiguration().get("corpus_size").trim());
			String outwardLinks = "";

			for (PairOfStringInt v : values) {
				if (v.getRightElement() == 0)
					newScore += Float.parseFloat(v.getLeftElement());
				else if(v.getRightElement() == 1){
					if (!outwardLinks.contains(v.getLeftElement()))
						outwardLinks += v.getLeftElement();
				}else if(v.getRightElement() == 2){
					oldScore = Float.parseFloat(v.getLeftElement());
				}
			}
			newScore = (epsilon / corpusSize) + ((1 - epsilon) * newScore);
			mKey.set(key.toString());
			mValue.set("--"+newScore+"--"+oldScore+outwardLinks);
			context.write(mKey, mValue);
		}
	}

	/*
	* Mapper for job 4
	* Outputs a blank key and the pageRank value for each node
	* The key is left blank so all pageRank values will be grouped into the
	* same
	* reducer to calculate the normalization value
	*/
	private static class NormalizeJ4Mapper extends Mapper<Object, Text, Text, FloatWritable> {
		private Text blankText = new Text("");
		private FloatWritable normVal = new FloatWritable();

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

			String values[] = value.toString().replaceAll("\\s", "").split("--");
			normVal.set(Float.parseFloat(values[1]));
			context.write(blankText, normVal);
		}
	}

	/*
	* Reducer for job 4
	* Calculate the normalization value
	* Outputs said normalization value that is used to normalize pageRank
	* values
	*/
	private static class NormalizeJ4Reducer extends Reducer<Text, FloatWritable, Text, Text> {
		private Text blankKey = new Text();
		private Text normVal = new Text();

		public void reduce(Text key, Iterable<FloatWritable> values, Context context) throws IOException, InterruptedException {

			float div = 0;
			float max = 0;
			
			for (FloatWritable rank : values) {
				if (max < rank.get())
					max = rank.get();
				div += rank.get();
			}
			normVal.set(Float.toString(1 / div));
			context.write(blankKey, normVal);
		}
	}

	/*
	* Mapper for job 5
	* Outputs updated row in our pageRank list after being normalized
	*/
	private static class NormalizeJ5Mapper extends Mapper<Object, Text, Text, Text> {
		private Text mKey = new Text();
		private Text blankValue = new Text();

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

			String outwardLinks = "--";
			String values[] = value.toString().replaceAll("\\s", "").split("--");
			String pageTitle = values[0];
			float normalize = Float.parseFloat(context.getConfiguration().get("normalize").trim());
			float newPageRank = Float.parseFloat(values[1]) * normalize;
			float oldPageRank = Float.parseFloat(values[2]);
			
			for(int i = 3; i<values.length; i++){
				outwardLinks+=values[i]+"--";
			}
			
			mKey.set(pageTitle+ "--"+newPageRank+"--"+oldPageRank+ outwardLinks);
			context.write(mKey, blankValue);
		}

	}

	/*
	* Reducer for job 5
	* Outputs the key that was built from the mapper, that re publishes the
	* pageRanking
	* after being normalized.
	*/
	private static class NormalizeJ5Reducer extends Reducer<Text, Text, Text, Text> {
		private Text blankValue = new Text("");

		public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
			context.write(key, blankValue);
		}
	}

	/*
	* Mapper for job 6
	* Outputs the negated pageRank and pageTitle
	* We negate the page rank to reverse the order so it will be descending
	*/
	private static class FinalOutputJ6Mapper extends Mapper<Object, Text, FloatWritable, Text> {
		private FloatWritable rankScore = new FloatWritable();
		private Text wikiPage = new Text();

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {		
			String values[] = value.toString().replaceAll("\\s", "").split("--");
			String pageTitle = values[0];
			float pageRank = Float.parseFloat(values[1]);

			rankScore.set(pageRank * -1);
			wikiPage.set(pageTitle);
			context.write(rankScore, wikiPage);
		}

	}

	/*
	* Reducer for job 6
	* Outputs pageTitle and Rank in descending order by rank
	*/
	private static class FinalOutputJ6Reducer extends Reducer<FloatWritable, Text, Text, Text> {
		public void reduce(FloatWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
			for (Text page : values) {
				context.write(page, new Text(new BigDecimal(key.toString().replaceFirst("-", "")).toString()));
			}
		}
	}
	
	/*
	 * Job 7
	 * tests for convergence
	 */
	private static class ConvergenceJ7Mapper extends Mapper<Object, Text, Text, FloatWritable> {
		private FloatWritable rankScore = new FloatWritable();
		private Text blankKey = new Text("");

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {		
			String values[] = value.toString().replaceAll("\\s", "").split("--");
			float newPageRank = Float.parseFloat(values[1]);
			float oldPageRank = Float.parseFloat(values[2]);
			float epsilon = Float.parseFloat(context.getConfiguration().get("epsilon"));

			
			newPageRank-=oldPageRank;
			newPageRank = Math.abs(newPageRank);
			if(newPageRank < epsilon){
				rankScore.set(1.0f);
				context.write(blankKey, rankScore);
			}else{
				rankScore.set(0.0f);
				context.write(blankKey, rankScore);
			}
		}

	}

	/*
	* Reducer for job 6
	* Outputs pageTitle and Rank in descending order by rank
	*/
	private static class ConvergenceJ7Reducer extends Reducer<Text, FloatWritable, Text, Text> {
		private Text blankValue = new Text();
		private Text cResult = new Text();
		public void reduce(Text key, Iterable<FloatWritable> values, Context context) throws IOException, InterruptedException {
			boolean converge = true;
			
			for(FloatWritable fl : values){
				if(fl.get() == 0.0f) converge = false;
			}
			if(converge) cResult.set("1");
			else cResult.set("0");
			context.write(cResult, blankValue);
		}
	}

	/*
	* Will clean up extraneous folders that could potentially be created
	* in the case that we exit the driver prematurely.
	*/
	public static void removeIntermediateOutput(int x, String[] otherArgs, Configuration conf) throws IllegalArgumentException, IOException {
		FileSystem.get(conf).delete(new Path(otherArgs[1] + "_normalize"), true);
		FileSystem.get(conf).delete(new Path(otherArgs[1] + "_corpusSize"), true);
		FileSystem.get(conf).delete(new Path(otherArgs[1] + "_norm"), true);
		FileSystem.get(conf).delete(new Path(otherArgs[1] + "_pageRank"), true);
		FileSystem.get(conf).delete(new Path(otherArgs[1] + "_converge"), true);

	}

	/*
	* Performs multiple page rank iterations, and cleans up extraneous output
	* after each iteration
	*/
	public static boolean multiPR(int x, String[] otherArgs, Configuration conf) throws FileNotFoundException, Exception {
		for (int i = 0; i < x; i++) {
			System.out.println("\n\n\t\t\t\t Iteration: " + i + "\n\n\n");
			doJob3(otherArgs, conf, otherArgs[1] + "_norm", otherArgs[1] + "_pageRank");
			FileSystem.get(conf).delete(new Path(otherArgs[1] + "_norm"), true);
			
			doJob4(otherArgs, conf, otherArgs[1] + "_pageRank", otherArgs[1] + "_normalize");
			
			doJob5(otherArgs, conf, otherArgs[1] + "_pageRank", otherArgs[1] + "_norm");
			FileSystem.get(conf).delete(new Path(otherArgs[1] + "_pageRank"), true);
			
		}
		return true;
	}
	
	/*
	* Tests output of job 5 to determine if the output has converged
	*/
	public static boolean Convergence(String[] otherArgs, Configuration conf) throws FileNotFoundException, Exception {
		int i=0;
		while(true){
			System.out.println("\n\n\t\t\t\t Iteration: " + i + "\n\n\n");
			doJob3(otherArgs, conf, otherArgs[1] + "_norm", otherArgs[1] + "_pageRank");
			FileSystem.get(conf).delete(new Path(otherArgs[1] + "_norm"), true);
			
			doJob4(otherArgs, conf, otherArgs[1] + "_pageRank", otherArgs[1] + "_normalize");
			
			doJob5(otherArgs, conf, otherArgs[1] + "_pageRank", otherArgs[1] + "_norm");
			FileSystem.get(conf).delete(new Path(otherArgs[1] + "_pageRank"), true);
			

			doJob7(otherArgs, conf, otherArgs[1] + "_norm", otherArgs[1] + "_converge");
			FileSystem fs = FileSystem.get(conf);
			BufferedReader br = new BufferedReader(new InputStreamReader(fs.open(new Path(otherArgs[1]+"_converge/part-r-00000"))));
			String result = br.readLine().trim();
			br.close();
			FileSystem.get(conf).delete(new Path(otherArgs[1]+"_converge"), true);
			if(result.equals("1")){ 
				break;
			}
			i++;
		}
		return true;
	}

	/*
	* Partitioner for Job 1, to ensure correct mapper output will make it to
	* the same reducer
	* I.e. ((p,0), p) and ((p,1), q) will reduce the same
	*/
	private static class customPartitioner extends Partitioner<PairOfStringInt, Text> {
		public int getPartition(PairOfStringInt key, Text value, int numReduceTasks) {
			return Math.abs((key.getLeftElement().hashCode()) % numReduceTasks);
		}
	}

	/*
	* Function that performs Job 1
	* build link graphs
	*/
	public static boolean doJob1(String[] otherArgs, Configuration conf) throws Exception {
		// remove files from last run
		FileSystem.get(conf).delete(new Path(otherArgs[1]), true);
		FileSystem.get(conf).delete(new Path(otherArgs[1] + "_norm"), true);

		Job job = Job.getInstance(conf);
		job.setNumReduceTasks(8);
		job.setPartitionerClass(customPartitioner.class);
		job.setJarByClass(PageRank.class);
		job.setMapperClass(LinkGraphJ1Mapper.class);
		job.setReducerClass(LinkGraphJ1Reducer.class);

		job.setOutputKeyClass(PairOfStringInt.class);
		job.setOutputValueClass(Text.class);

		FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
		FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));

		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}

	/*
	* Function that performs Job 1.5
	* Corpus size
	*/
	public static boolean doJob1_5(String[] otherArgs, Configuration conf) throws Exception {
		Job job = Job.getInstance(conf);
		job.setJarByClass(PageRank.class);
		job.setMapperClass(CorpusSizeJ1_5Mapper.class);
		job.setReducerClass(CorpusSizeJ1_5Reducer.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
		FileOutputFormat.setOutputPath(job, new Path(otherArgs[1] + "_corpusSize"));

		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}

	/*
	* Function that performs Job 2
	* builds base pageRank with initial PR values
	*/
	public static boolean doJob2(String[] otherArgs, Configuration conf) throws Exception {
		// read in corpusSize from previous job and put it in configuration
		FileSystem fs = FileSystem.get(conf);
		BufferedReader br = new BufferedReader(new InputStreamReader(fs.open(new Path(otherArgs[1] + "_corpusSize/part-r-00000"))));
		conf.set("corpus_size", br.readLine());
		br.close();
		FileSystem.get(conf).delete(new Path(otherArgs[1] + "_corpusSize"), true);

		Job job = Job.getInstance(conf);
		job.setNumReduceTasks(8);
		job.setJarByClass(PageRank.class);
		job.setMapperClass(LinkGraphJ2Mapper.class);
		job.setReducerClass(LinkGraphJ2Reducer.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		FileInputFormat.addInputPath(job, new Path(otherArgs[1]));
		FileOutputFormat.setOutputPath(job, new Path(otherArgs[1] + "_norm"));

		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}

	/*
	* Function that performs Job 3
	* does page rank iteration
	*/
	public static boolean doJob3(String[] otherArgs, Configuration conf, String input, String output) throws Exception {
		// cleanup original output directory for final output
		FileSystem.get(conf).delete(new Path(otherArgs[1]), true);

		Job job = Job.getInstance(conf);
		job.setNumReduceTasks(8);
		job.setJarByClass(PageRank.class);
		job.setMapperClass(PageRankJ3Mapper.class);
		job.setReducerClass(PageRankJ3Reducer.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(PairOfStringInt.class);

		FileInputFormat.addInputPath(job, new Path(input));
		FileOutputFormat.setOutputPath(job, new Path(output));

		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}

	/*
	* Function that performs Job 4
	* find normalization value
	*/
	public static boolean doJob4(String[] otherArgs, Configuration conf, String input, String output) throws Exception {
		Job job = Job.getInstance(conf);
		job.setJarByClass(PageRank.class);
		job.setMapperClass(NormalizeJ4Mapper.class);
		job.setReducerClass(NormalizeJ4Reducer.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(FloatWritable.class);

		FileInputFormat.addInputPath(job, new Path(input));
		FileOutputFormat.setOutputPath(job, new Path(output));

		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}

	/*
	* Function that performs Job 5
	* Normalizes page rank value for this iteration
	*/
	public static boolean doJob5(String[] otherArgs, Configuration conf, String input, String output) throws Exception {
		//reads normalize value and adds it to configurations
		FileSystem fs = FileSystem.get(conf);
		BufferedReader br = new BufferedReader(new InputStreamReader(fs.open(new Path(otherArgs[1] + "_normalize/part-r-00000"))));
		conf.set("normalize", br.readLine());
		br.close();
		FileSystem.get(conf).delete(new Path(otherArgs[1] + "_normalize"), true);

		Job job = Job.getInstance(conf);
		job.setNumReduceTasks(8);
		job.setJarByClass(PageRank.class);
		job.setMapperClass(NormalizeJ5Mapper.class);
		job.setReducerClass(NormalizeJ5Reducer.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		FileInputFormat.addInputPath(job, new Path(input));
		FileOutputFormat.setOutputPath(job, new Path(output));

		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}

	/*
	* Function that performs Job 6
	* Organizes output, Descending by page rank value
	*/
	public static boolean doJob6(String[] otherArgs, Configuration conf, String input, String output) throws Exception {
		FileSystem.get(conf).delete(new Path(otherArgs[1]), true);

		Job job = Job.getInstance(conf);
		job.setJarByClass(PageRank.class);
		job.setMapperClass(FinalOutputJ6Mapper.class);
		job.setReducerClass(FinalOutputJ6Reducer.class);

		job.setOutputKeyClass(FloatWritable.class);
		job.setOutputValueClass(Text.class);

		FileInputFormat.addInputPath(job, new Path(input));
		FileOutputFormat.setOutputPath(job, new Path(output));

		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}
	
	public static boolean doJob7(String[] otherArgs, Configuration conf, String input, String output) throws Exception {
		FileSystem.get(conf).delete(new Path(otherArgs[1]), true);

		Job job = Job.getInstance(conf);
		job.setJarByClass(PageRank.class);
		job.setMapperClass(ConvergenceJ7Mapper.class);
		job.setReducerClass(ConvergenceJ7Reducer.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(FloatWritable.class);

		FileInputFormat.addInputPath(job, new Path(input));
		FileOutputFormat.setOutputPath(job, new Path(output));

		return (job.waitForCompletion(true) ? Boolean.TRUE : Boolean.FALSE);
	}
}
