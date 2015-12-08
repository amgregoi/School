import java.text.*;

public class Mortgage {

	private double rate;
	private double term;
	private double amount;
	private double monthlyPayment;
	private double totalPayment;
	
	public Mortgage(double r, double t, double a){
		rate = r;
		term = t;
		amount = a;
	}
	
	public Mortgage(){
		rate=5.5/100;
		term=15;
		amount=100000;
	}
	
	
	/**
	* (Calculate and set the monthly payment for the loan)
	*
	* @param1 (Rate - Interest Rate )
	* @param2 (Term - length of time to pay back loan)
	* @param3 (Amount - Total amount of loan you took out)
	* @return (Returns how much you will have to pay each month to pay back your loan)
	*/
	public void setMonthlyPayment(){
		double num1 = amount*(rate/12);
	    double num2 = (1-(Math.pow(1/(1+(rate/12)),term*12)));
		monthlyPayment = num1/num2;		
	}
	
	/**
	* ( Calculate and set the total payment for the loan)
	*
	* @param1 (monthlyPayment - how much you will have to pay each month to pay back your loan)
	* @param2 (Term - length of time to pay back loan)
	* @return (returns the total amount you will pay back at the end of paying off your loan)
	*/
	public void setTotalPayment(){
		totalPayment = monthlyPayment*term*12;
	}
	
	/**
	* (Display formatted output of Monthly payment and Total Payment values)
	*
	* @param (N/A)
	* @return (N/A)
	*/
	public void displayInfo(){
		DecimalFormat df = new DecimalFormat("#,###,000.00");
		System.out.println("monthly payment : $"+df.format(monthlyPayment));
		System.out.println("total payment : $"+df.format(totalPayment));
		System.out.println();
	}
}