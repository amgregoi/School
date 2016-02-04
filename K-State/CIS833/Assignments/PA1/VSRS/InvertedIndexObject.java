import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.io.ArrayWritable;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.io.WritableUtils;

import edu.umd.cloud9.io.ArrayListWritable;
import edu.umd.cloud9.io.PairOfStringFloat;

public class InvertedIndexObject implements Writable, Cloneable{
	private Text word;
	private IntWritable docFreq;
	private FloatWritable docLength;
	private FloatWritable IDF;
	ArrayListWritable<PairOfStringFloat> index;
	ArrayWritable temp;

	public InvertedIndexObject(String w, int freq) {
		word = new Text(w);
		docFreq = new IntWritable(freq);
		index = new ArrayListWritable<PairOfStringFloat>();
		temp = new ArrayWritable(PairOfStringFloat.class);
		docLength = new FloatWritable();
		IDF = new FloatWritable();
		
	}
	
	public InvertedIndexObject()
	{
		word = new Text();
		docFreq = new IntWritable();
		index = new ArrayListWritable<PairOfStringFloat>();
		temp = new ArrayWritable(PairOfStringFloat.class);
		docLength = new FloatWritable();
		IDF = new FloatWritable();

	}

	public Text getWord() {
		return word;
	}

	public void setWord(Text w) {
		this.word = w;
	}

	public IntWritable getDF() {
		return docFreq;
	}

	public void setDF(IntWritable df) {
		this.docFreq = df;
	}
	
	public FloatWritable getDocLength()
	{
		return docLength;
	}

	public void setDocLength(FloatWritable fw)
	{
		this.docLength = fw;
	}
	
	public void setIDF(FloatWritable f)
	{
		this.IDF = f;
	}
	
	public FloatWritable getIDF(){
		return this.IDF;
	}
	


	public void addToIndex(String doc, float tf) {
		index.add(new PairOfStringFloat(doc, tf));
	}

	public void addToIndex(PairOfStringFloat pair) {
		index.add(pair);
	}

	public ArrayListWritable<PairOfStringFloat> getIndex() {
		return index;
	}

	public Float getIndexWeight(String doc) {
		for(PairOfStringFloat p : index)
			if(p.getLeftElement().equals(doc))
				return p.getRightElement();
		return -1.0f;
	}

	public void setIndex(ArrayListWritable<PairOfStringFloat> p) {
		this.index = p;
	}
	

	@Override
	public void write(DataOutput out) throws IOException {
		// TODO Auto-generated method stub
		word.write(out);
		docFreq.write(out);
		docLength.write(out);
		IDF.write(out);
		Writable[] t = new Writable[index.size()];
		for(int i=0; i<index.size(); i++)
		{
			t[i] = index.get(i);
		}
		temp = new ArrayWritable(PairOfStringFloat.class, t);
		temp.write(out);
	}

	@Override
	public void readFields(DataInput in) throws IOException {
		// TODO Auto-generated method stub
		word.readFields(in);
		docFreq.readFields(in);
		docLength.readFields(in);
		IDF.readFields(in);
		temp.readFields(in);
		index = new ArrayListWritable<PairOfStringFloat>();
		Writable[] writables=temp.get();
		  for (int i=0; i < writables.length; i++) {
		    index.add((PairOfStringFloat)writables[i]);
		  }
	}

}
