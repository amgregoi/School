import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.StringTokenizer;

import org.apache.hadoop.io.FloatWritable;

import edu.umd.cloud9.io.PairOfStringFloat;

public class lookup {

	String index;
	HashMap<String, Float> documents;
	int numDocs;
	Stemmer stem;

	public lookup(String index, int docCount) throws IOException {
		this.index = index;
		numDocs = docCount;
		stem = new Stemmer();
	}

	public InvertedIndexObject findInput(String input) throws IOException {

		FileReader file = new FileReader(index);
		BufferedReader bf = new BufferedReader(file);
		String line;
		stem.add(input.toCharArray(), input.length());
		stem.stem();
		input = stem.toString();
		InvertedIndexObject iio = null;
		while ((line = bf.readLine()) != null) {
			StringTokenizer st = new StringTokenizer(line,
					" \t\n\r\f,:;?![]'!@#$%^&*()_+-=\\/");
			String s = st.nextToken();
			if (s.equals(input)) {
				int df = Integer.parseInt(st.nextToken());
				iio = new InvertedIndexObject(s, df);
				while (st.hasMoreElements()) {
					String docNum = st.nextToken();
					BigDecimal tf = new BigDecimal(st.nextToken());
					iio.addToIndex(new PairOfStringFloat(docNum, tf
							.floatValue()));
				}
			}
		}
		bf.close();

		return iio;
	}

	public ArrayList<InvertedIndexObject> findTermsByDoc(String doc) throws NumberFormatException, IOException {

		ArrayList<InvertedIndexObject> result = new ArrayList<>();
		FileReader file = new FileReader(index);
		BufferedReader bf = new BufferedReader(file);
		String line;
		while ((line = bf.readLine()) != null) {
			StringTokenizer st = new StringTokenizer(line,
					" \t\n\r\f,:;?![]'!@#$%^&*()_+-=\\/");
			String s = st.nextToken();
			int df = Integer.parseInt(st.nextToken());
			InvertedIndexObject iio = new InvertedIndexObject(s, df);
			while (st.hasMoreElements()) {
				String docNum = st.nextToken();
				BigDecimal tf = new BigDecimal(st.nextToken());
				iio.addToIndex(new PairOfStringFloat(docNum, tf.floatValue()));
				if(docNum.equals(doc))
				{
					result.add(iio);
					break;
				}
			}

		}
		bf.close();
		return result;
	}

	public InvertedIndexObject partialQuery(String input) throws IOException {
		InvertedIndexObject iio;
		stem.add(input.toCharArray(), input.length());
		stem.stem();
		String stemInput = stem.toString();
		iio = findInput(stemInput);

		BigDecimal num = new BigDecimal(Math.log10(numDocs / iio.getDF().get()))
				.setScale(4, RoundingMode.HALF_UP);
		BigDecimal denom = new BigDecimal(Math.log10(2)).setScale(4,
				RoundingMode.HALF_UP);
		BigDecimal IDF = new BigDecimal(num.floatValue() / denom.doubleValue())
				.setScale(10, RoundingMode.HALF_UP);

		iio.setIDF(new FloatWritable(IDF.floatValue()));
		return iio;
	}
}
