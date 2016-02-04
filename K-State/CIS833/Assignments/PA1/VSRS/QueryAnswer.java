import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Scanner;
import java.util.SortedSet;
import java.util.StringTokenizer;
import java.util.TreeMap;
import java.util.TreeSet;

import edu.umd.cloud9.io.PairOfStringFloat;
import edu.umd.cloud9.io.Tuple;
import edu.umd.cloud9.io.TupleException;
import edu.umd.cloud9.util.Histogram;
import edu.umd.cloud9.util.MapKI;
import edu.umd.cloud9.util.MapKI.Entry;

public class QueryAnswer {

	public QueryAnswer()
	{
		
	}
	
	public static HashMap<String, Float> buildDocs(String path)
			throws IOException {
		HashMap<String, Float> index = new HashMap<>();

		FileReader file = new FileReader(path);
		BufferedReader bf = new BufferedReader(file);
		String line;
		while ((line = bf.readLine()) != null) {
			StringTokenizer st = new StringTokenizer(line,
					" \t\n\r\f,:;?![]'!@#$%^&*()_+-=\\/");
			String s = st.nextToken();
			float length = Float.parseFloat(st.nextToken());
			index.put(s, length);
		}
		bf.close();

		return index;
	}

	public static int getDocCount(String path) throws IOException {
		FileReader file = new FileReader(path);
		BufferedReader bf = new BufferedReader(file);
		String line;
		if ((line = bf.readLine()) != null) {
			StringTokenizer st = new StringTokenizer(line,
					" \t\n\r\f,:;?![]'!@#$%^&*()_+-=\\/");
			int numDocs = Integer.parseInt(st.nextToken());
			bf.close();
			return numDocs;
		}
		bf.close();
		return 0;

	}

	public void query(String index, String numDoc, String docLength) throws IOException {

		int docCount = getDocCount(numDoc);
		lookup look = new lookup(index, docCount);
		Scanner scanner = new Scanner(System.in);
		Histogram<String> termCount = new Histogram<String>();
		HashMap<String, Float> query = new HashMap<String, Float>();
		HashMap<String, Float> documents = buildDocs(docLength);// key for
																// documents is
																// documentNo
		if (documents == null) {
			System.out.println("Document Length file invalid");
			System.exit(-1);
		}

		InvertedIndexObject iio;
		while (true) {
			termCount.clear();
			HashMap<String, ArrayList<PairOfStringFloat>> relDocs = new HashMap<>();
			System.out.print("Enter query (-1 to exit): ");
			String input = scanner.nextLine();
			if (input.equals("-1")) {
				break;
			}

			StringTokenizer st = new StringTokenizer(input);
			//constructs map of relevant documents containing words in our query
			while (st.hasMoreTokens()) {
				String token = st.nextToken();
				iio = look.findInput(token);
				if (iio == null) {
					continue;
				}
				termCount.count(token);
				for (PairOfStringFloat p : iio.getIndex()) {
					if (!relDocs.containsKey(p.getLeftElement())) {
						ArrayList<PairOfStringFloat> t = new ArrayList<>();
						relDocs.put(p.getLeftElement(), t);
					}
				}
			}
			
			//gets max(tf) of query to calculate idf
			int maxQuery = 0;
			for (Entry<String> e : termCount.entrySet()) {
				if (e.getValue() > maxQuery)
					maxQuery = e.getValue();
			}
			
			
			//
			// builds tf-idf list for each document needed or cosine similarity
			Iterator i = relDocs.entrySet().iterator();
			while (i.hasNext()) {
				Map.Entry pair = (Map.Entry) i.next();
				ArrayList<InvertedIndexObject> wordsForDoc = look
						.findTermsByDoc(pair.getKey().toString());
				float posf;
				ArrayList<PairOfStringFloat> holder = relDocs
						.get(pair.getKey());
				for (InvertedIndexObject obj : wordsForDoc) {
					if (!((posf = obj.getIndexWeight(pair.getKey().toString())) == -1.0f)) {
						holder.add(new PairOfStringFloat(obj.getWord()
								.toString(), posf));
					}
				}
			}
			
			
			float query_denom = 0.0f;
			//builds tf-idf for query
			Stemmer stem = new Stemmer();
			for (Entry<String> p : termCount.entrySet()) {
				String word = p.getKey();
				int count = termCount.get(word);
				int numDocsWordIn = look.findInput(word).getIndex().size();
				BigDecimal tf = new BigDecimal(count/(double)maxQuery).setScale(4, RoundingMode.HALF_UP);
				BigDecimal idf = new BigDecimal(Math.log(docCount/numDocsWordIn)/Math.log(2)).setScale(4, RoundingMode.HALF_UP);
				BigDecimal tf_idf = new BigDecimal(tf.floatValue() * idf.floatValue()).setScale(4, RoundingMode.HALF_UP);
				stem.add(word.toCharArray(), word.length());
				stem.stem();
				word = stem.toString();
				query.put(word, tf_idf.floatValue());
				query_denom += Math.pow(tf_idf.floatValue(), 2);
				//System.out.println(word + " \t" + tf.floatValue() + " \t" + idf.floatValue() + " \t " + tf_idf.floatValue());
			}

			
			//calculate cosine similarity
			SortedSet<String> keys = new TreeSet<String>(relDocs.keySet());

			
			TreeMap<Float, String> treeMap = new TreeMap<Float, String>();
			Iterator d = relDocs.entrySet().iterator();
			while (d.hasNext()) {										//per document
				Map.Entry pair = (Map.Entry) d.next();
				ArrayList<PairOfStringFloat> hold = relDocs.get(pair.getKey());
				//document half of denom
				float doc_denom = 0.0f;
				for(PairOfStringFloat p : hold)							// grabs list of words per document
				{
					doc_denom += Math.pow(p.getRightElement(), 2);
				}
				float denom = new BigDecimal(Math.sqrt(doc_denom*query_denom)).floatValue();
				float numer = 0.0f;
				for(PairOfStringFloat p : hold)							
				{
					if(query.containsKey(p.getLeftElement()))
					{
						numer += p.getRightElement() * query.get(p.getLeftElement());
					}
				}
				BigDecimal cos = new BigDecimal(numer/denom).setScale(10, RoundingMode.HALF_UP);
				treeMap.put(cos.floatValue(), pair.getKey().toString());
			}
			
			//bad work around, assuming no two cos similarities will be the exact same
			int count = 1;
			for(Float sim : treeMap.descendingKeySet())
			{
				String doc = treeMap.get(sim);
				BigDecimal p = new BigDecimal(count/Double.parseDouble(doc)).setScale(5, RoundingMode.HALF_UP);
				BigDecimal r = new BigDecimal(count/10.0f).setScale(5, RoundingMode.HALF_UP);
				System.out.println("\tcranfield"+doc + "\t score: " + sim + "\t P = " + p + "\t R = " + r);
				count++;
				if(count > 10)
				{
					break;
				}
			}
		}

		scanner.close();

	}
}
