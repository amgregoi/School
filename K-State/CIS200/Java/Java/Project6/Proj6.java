/**
* (Calculates fractional operations)
*
* @author (Andy Gregoire)
* @version (Project 6)
*/
import java.util.*;	

public class Proj6 {
	public static void main(String[] args) {
		Scanner s = new Scanner(System.in);

		boolean cont = true;
		String str = "";
	while(cont){
		System.out.println("Enter 'e' to exit program");
		System.out.print("Enter the expresion (like 2/3 + 3/4): ");
		str = s.nextLine();
		String delims1 = "[+\\-*/ ]+";		// split delimiters v1
		String delims2 = "[0123456789 ]+";	// split delimiters v2
		String[] sign = str.split(delims2); // Holds onto operation signs
		String[] nums = str.split(delims1); // holds numerator / denominator values
		char[] test = str.toCharArray();
		//Exiting loop
		if(test[0] == 'e' || test[0] == 'E'){ 
			System.out.println("Exiting Program");
			break;
			}
		int f1n =Integer.parseInt(nums[0]); int f1d =Integer.parseInt(nums[1]);
		int f2n =Integer.parseInt(nums[2]); int f2d =Integer.parseInt(nums[3]);
		
//###########  Simplifies original fractions #############
		for(int i=2; i< f1d; i++){
			if(f1n%i == 0 && f1d%i ==0){
				f1n/=i;
				f1d/=i;
				i=1;
			}
		}
		for(int i=2; i< f2d; i++){
			if(f2n%i == 0 && f2d%i ==0){
				f2n/=i;
				f2d/=i;
				i=1;
			}
		}
//########### End Simplification ############

		Fraction f1 = new Fraction(f1n, f1d);
		Fraction f2 = new Fraction(f2n, f2d);
		Fraction output = new Fraction();
		
		System.out.println();
		System.out.print("	" +f1 +" "+ sign[2]+ " " + f2 +" = ");
		
//########### Calls Operations ##############
		if(sign[2].equals("+"))
			output = f2.plus(f1);
		else if(sign[2].equals("-"))
			output = f2.minus(f1);
		else if(sign[2].equals("/"))
			output = f2.divide(f1);
		else if(sign[2].equals("*"))
			output = f2.times(f1);
			
		System.out.println(output);	
		System.out.println();
	}
		
	}
}