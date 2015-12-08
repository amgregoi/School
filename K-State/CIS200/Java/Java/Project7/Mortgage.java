import java.text.DecimalFormat;

/**
 * Mortgage.java
 * Used to define a Mortgage object consisting of an annual interest rate,
 * the number of years for the loan and the loan amount. Contains methods to
 * calculate the monthly loan payment and the total amount paid.
 * Andy Gregoire
 * Project 7
*/

public class Mortgage
{
  private double annualInterestRate;
  private int numOfYears;
  private double loanAmount;
  private double monthlyPayment;
  private double totalPayment;

  // Default constructor - sets a 100,000 loan at 5.5% for 15 years
  // Used for Advertised Promotion
  public Mortgage()
  { this (5.5, 15, 100000);			// calls 3-arg constructor below
  } // end Mortgage() constructor

  // Construct a mortgage with specified annual interest rate,
  // number of years and loan amount
  public Mortgage(double newInterestRate, int newNumOfYears,
                  double newLoanAmount)
  { annualInterestRate = newInterestRate;
    numOfYears = newNumOfYears;
    loanAmount = newLoanAmount;
  } // end 3-argument constructor

// ------------------ Monthly Payment ---------------------
  // returns the value for the private data property monthlyPayment
  // currently not used...
  public double getMonthlyPayment()
  { return 	monthlyPayment;
  } // end getMonthlyPayment

  // Calculate and set the monthly payment for the loan
  public void setMonthlyPayment()
  { double monthlyInterestRate = annualInterestRate/1200;

	monthlyPayment = loanAmount*monthlyInterestRate/
      (1 - (Math.pow(1/(1 + monthlyInterestRate), numOfYears*12)));
  } // end setMonthlyPayment

// ------------------ Total Payment ---------------------
  // returns the value for the private data property totalPayment
  // currently not used...
  public double getTotalPayment()
  { return 	totalPayment;
  } // end getMonthlyPayment

  // Calculate and set the total amount to be paid on the loan
  public void setTotalPayment()
  { totalPayment = monthlyPayment * numOfYears * 12;
  } // end totalPayment

// ------------------ Display Output ---------------------
  public String toString()
  { // *** Must import java.text.DecimalFormat ***
    // Following only display 2 values after decimal if non-zero
    // DecimalFormat df = new DecimalFormat("$###,###.##");

    // Following ALWAYS display 2 values after decimal
    DecimalFormat df = new DecimalFormat("$#,###,###.00");
	return("The monthly payment is " + df.format(monthlyPayment) + 
	 "\nThe total payment is " + df.format(totalPayment));
	
  } // end displayInfo

} // end class
