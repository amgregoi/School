public class Fraction {

	private int num;
	private int den;
	
	public Fraction(int n, int d){
		num = n;
		den = d;
	}
	public Fraction(){
		num = 0;
		den = 0;
	}
	
	public String toString(){ // used to display a fraction
		return (num + "/" + den);
	}
	
/**
* (Adds the two fractions)
*
* @param (fraction the operation is being applied to)
* @return (output fraction)
*/
	public Fraction plus(Fraction f){ // adds 2 fractions and returns reduce fraction result
	
		if(f.den != den){
			f.num*= den;
			num*= f.den;
			f.den*= den;
			den = f.den;
		}
		
		f.num += num;
		f.reduce();
		return f;
	}
/**
* (Subtracts the two fractions)
*
* @param (fraction the operation is being applied to)
* @return (output fraction)
*/
	public Fraction minus(Fraction f){ // subtracts 2 fractions and returns reduce fraction result
	
		if(f.den != den){
			f.num*= den;
			num*= f.den;
			f.den*= den;
			den = f.den;
		}
		
		f.num -= num;
		f.reduce();
		return f;
	}
	
/**
* (Multiplies the two fractions)
*
* @param (fraction the operation is being applied to)
* @return (output fraction)
*/
	public Fraction times(Fraction f){ // multiplies 2 fractions and returns reduce fraction result
		f.num*=num;
		f.den*=den;
		f.reduce();
		return f;
	}
	
/**
* (Divides the two fractions)
*
* @param (fraction the operation is being applied to)
* @return (output fraction)
*/
	public Fraction divide(Fraction f){ // divides 2 fractions and returns reduce fraction result
		f.num*= den;
		f.den*= num;
		f.reduce();
		return f;
	}
	
	/**
* (Simplifying output fraction)
*
* @param (None)
* @return (None)
*/
	private void reduce ( ){ // modifies num/denom so fraction reduced to lowest terms
		for(int i=2; i< den; i++){
			if(num%i == 0 && den%i ==0){
				num/=i;
				den/=i;
				i=1;
			}
			//System.out.println("Num: " + num + " Den: " + den);
		}
	}
 



}
