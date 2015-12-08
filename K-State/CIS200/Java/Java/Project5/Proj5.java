/**
* (Calculates monthly payments and total payment of a loan based on unique or set promotional values)
*
* @author (Andy Gregoire)
* @version (Project 5)
*/
import java.util.*;
import java.text.*;	

public class Proj5 {
	public static void main(String[] args) {
		Scanner s = new Scanner(System.in);
		char x = 0;    // enable validation if they enter characters other than Ints
		while(x!=51){
			index();
			x = s.nextLine().charAt(0);
			System.out.println();
			
			if((int)x == 49){
				promotion();
			}
			else if((int)x == 50){
				unique();
			}
			else if((int)x == 51){
				System.out.println("PROGRAM COMPLETE...");
				break;
			}
			else{
				System.out.println("Invalid choice, please re-enter");
				System.out.println();
			}
		}
		
		
		
	}
/**
	* (Prints intial index / menu of the program)
	*
	* @param (N/A)
	* @return (N/A)
	*/
	public static void index(){
		System.out.println("Please choose from the following choices");
		System.out.println("	1)Promotional Loan ($100,000 @ 5.5% for 15 years");
		System.out.println("	2)Unique Loan(enter in loan values");
		System.out.println("	3)Quit (Exit the program)");
		System.out.println();
		System.out.print("	Please enter your selection (1-3): ");
	}

//#############################  Promotional / unique outputs ###################################
	/**
	* (Promotional loan - this method just puts all the information together and outputs to screen)
	*
	* @param (N/A)
	* @return (N/A)
	*/
	public static void promotion(){
		Mortgage mort1 = new Mortgage();
		mort1.setMonthlyPayment();
		mort1.setTotalPayment();
		System.out.println("PROMOTIONAL LOAN...:");
		mort1.displayInfo();
	}
	/**
	* (Unique Loan  - this method just puts all the information together and outputs to screen)
	*
	* @param (N/A)
	* @return (N/A)
	*/
	public static void unique(){
		System.out.println("	Please enter the following information...");
		double rate=getRate()/100;
		double term=getTerm();
		double amount=getAmount();
		Mortgage mort1 = new Mortgage(rate, term, amount);
		mort1.setMonthlyPayment();
		mort1.setTotalPayment();
		System.out.println();  // Cosmetic
		System.out.println("UNIQUE LOAN...:");
		mort1.displayInfo();
	}
	
//##################################### X Credit ###########################################	
	/**
	* (reads in and validates interest rate … valid interest rates are between 1%-9% (inclusive))
	*
	* @param (N/A)
	* @return (Returns a valid Interest rate selected by user)
	*/
	public static double getRate(){
		Scanner s = new Scanner(System.in);
		double rate = 0;
		int test = 1;
		while(test == 1){
			System.out.println("		Valid Interest Rates (1%-9%): ");
			System.out.print("		Enter Interest Rate (Ex. 7.25): ");
			rate = Double.parseDouble(s.nextLine());
			System.out.println();
			if(rate>=1 && rate <=9)
				test = 0;
			else if( rate < 1 || rate >9){
				test = 1;
				System.out.println("		not a valid rate, please re-enter");
				}
		}
		return rate;
	}
	/**
	* (reads in and validates length of the loan … valid terms are 5-50 years (inclusive))
	*
	* @param (N/A)
	* @return (Returns a valid term selected by user)
	*/
	public static double getTerm(){
		Scanner s = new Scanner(System.in);
		double term = 0;
		int test = 1;
		while(test == 1){
			System.out.println("		valid lengths (5 - 50): ");
			System.out.print("		Enter length of term in years: ");
			term = Integer.parseInt(s.nextLine());
			System.out.println();
			if(term>4 && term <51)
				test = 0;
			else if( term <=4 || term >50){
				test = 1;
				System.out.println("		not a valid term, please re-enter");
				}
		}
		return term;
	}
	
	/**
	* (reads in and validates loan amount … valid amounts are $50,000 to 1 million (inclusive))
	*
	* @param (N/A)
	* @return (Returns a valid loan amount selected by user)
	*/
	public static double getAmount(){
		Scanner s = new Scanner(System.in);
		double amount = 0;
		int test = 1;
		while(test == 1){
			System.out.println("		Valid loan amounts (50000 - 1000000): ");
			System.out.print("		Enter loan amount without $ or commas: ");
			amount = Integer.parseInt(s.nextLine());
			System.out.println();
			if(amount>= 50000 && amount <= 1000000)
				test = 0;
			else if( amount <50000 || amount >1000000){
				test = 1;
				System.out.println("		not a valid term, please re-enter");
				}
		}
		return amount;
	}
	
}
