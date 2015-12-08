/**
* Handles Input / output for Proj 7
*
* @author Andy Gregoire
* @version Project 7
*/
import java.util.*;

public class io
{
	
	private Scanner s;
	private double interestRate;
	private int years;
	private double amount;
	public int choice;
	
/**
* scanner consturctor
*/
	public io() {	
		s = new Scanner(System.in);
	}

	// input - get input (choices: 1,2,3)	
	
	
	
	// --------- Optional EXTRA CREDIT Methods ---------------------------- 
// Read in and validate interest rate
/**
* gets input / validates the rate

* @return  the rate
*/
  public double getRate()
	{	
	try{
		Scanner in = new Scanner (System.in);
		System.out.print("  Enter yearly interest rate (Ex: 8.25): ");
		double interestRate = Double.parseDouble(s.nextLine());
		}catch(NumberFormatException ex){ interestRate = 10; }
		while (interestRate < 1 || interestRate > 9) {
			try{
			System.out.println("\tValid Interest Rates are 1% - 9%");
			System.out.print("\tPlease re-enter valid yearly interest rate (Ex: 8.25): ");
			interestRate = Double.parseDouble(s.nextLine());
			}catch(NumberFormatException ex){ interestRate = 10; }
		} // end while
		
		return interestRate;
	} // end getRate

// Read in and validate term of the loan (in years)
/**
* gets input / validates term of the loan

* @return  term in years
*/
  public int getTerm( )
	{	
		try{
		Scanner in = new Scanner (System.in);
		System.out.print("  Enter number of years for the loan (5-50): ");
		int years = Integer.parseInt(s.nextLine());
		}catch(NumberFormatException ex){ years = 1; }
		while (years < 5 || years > 50) {
		try{
			System.out.println("\tValid Loan Terms are 5-50");
			System.out.print("\tPlease re-enter valid number of years: ");
			years = Integer.parseInt(s.nextLine());
			}catch(NumberFormatException ex){ years = 1; }
		} // end while
		return years;
	} // end getTerm

// Read in and validate loan amount
/**
* gets input / validates amount of loan

* @return  Amount of loan
*/
  public double getAmount( )
	{	
		try{
		Scanner in = new Scanner (System.in);
		System.out.print("  Enter loan amount without $ or commas (Ex:120000): ");
		amount = Double.parseDouble(s.nextLine());
		}catch(NumberFormatException ex){ amount = 1; }
		while (amount < 50000 || amount > 1000000) {
			try{
			System.out.println("\tValid Loan Amounts are $50,000-$1,000,000");
			System.out.print("\tPlease re-enter loan amount without $ or commas (Ex:120000): ");
			amount = Double.parseDouble(s.nextLine());
			}catch(NumberFormatException ex){ amount = 1; }
		} // end while
		return amount;
	} // end getAmount
	
//#########################################################################
/**
* Prints menu

* @return nothing
*/
public int menu(){
	
      System.out.println("\nPlease choose from the following choices below:");
      System.out.println("\t1) Promotional Loan ($100,000 @ 5.5% for 15 years)");
      System.out.println("\t2) Unique Loan (enter in loan values)");
      System.out.println("\t3) Quit (Exit the program)");
      System.out.print("\n\tPlease enter your selection (1-3): ");
	  return Integer.parseInt(s.nextLine());
	
}
/**
* Calls methods for promotional loan

* @return nothing
*/
public void one(){
		Mortgage promoLoan = new Mortgage();

        // calc and set value for the monthly payment
		promoLoan.setMonthlyPayment();

        // calc and set value for the total payment
		promoLoan.setTotalPayment();

        // Display results with formatting
		System.out.println("\nPROMOTIONAL LOAN...:");
		System.out.println(promoLoan.toString());
		
}
/**
* calls methods to get, validate and calculate values for payment

* @return nothing
*/
public void two(){
	System.out.println("\nPlease enter in the following information...");

		// Read in and validate interest rate
		double interestRate = getRate();
		System.out.println();	// display a blank line

		// Read in and validate term of the loan (in years)
		int years = getTerm();
		System.out.println();	// display a blank line

		// Read in and validate loan amount
		double loanAmount = getAmount();
		System.out.println();	// display a blank line

		// Create a Mortgage object
		Mortgage uniqueLoan = new Mortgage(interestRate, years, loanAmount);

        // calc and set value for the monthly payment
		uniqueLoan.setMonthlyPayment();

        // calc and set value for the total payment
		uniqueLoan.setTotalPayment();

		// Display results w/formatting
		System.out.println("\nUNIQUE LOAN...:");
		System.out.println(uniqueLoan.toString());
}

/**
* get input for "choice"

* @return value for choice
*/
public int def(){
		System.out.print("\t\tInvalid Choice. Please select 1, 2, or 3: ");
		return Integer.parseInt(s.nextLine());
        
}
/**
* Prints Program complete

* @return nothing
*/
public void comp(){
	System.out.println("\nPROGRAM COMPLETE...");
}
}