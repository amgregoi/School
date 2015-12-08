/* MortgageDriver.java - Demonstrate the use of the Mortgage class

  Allows a bank officer to enter in all the input or use a
  special advertised promotion ($100,000 house loan for 15 years
  at the annual rate of 5.5%).

  Displays the monthly payment and the total amount paid on the loan
  Project 7
  Andy Gregoire
*/

import java.text.DecimalFormat;
import java.util.Scanner;

public class Proj7
{
  public static void main(String[] args)
  { 
	int choice = 4;
	io s = new io();
	

    do
    {
		try{
			choice = s.menu();
			
		}catch(NumberFormatException ex){ choice = 4;}
		
	  switch(choice){
        // validate choice

      case 1: //create a promotional loan
      { 
		s.one();
		break;
      } // end promo loan
     case 2: // Unique Loan Option
      { 
		s.two();
		break;
      } // end unqiue loan
	  case 3: break;
	  default:
      {
		try{
		choice = s.def();
		}catch(NumberFormatException ex){ choice = 4;}
      } // end validate choice
	}
  } while (choice != 3);

  s.comp();
 }// end main
}//end MortgageDriver class
