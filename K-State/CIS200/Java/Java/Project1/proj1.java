/**
* (ASCII Name / Grade Average / Pizza slice rations)
*
* Author: (Andy Gregoire)
* Project: (Project1)
*/

import java.util.*;
import java.text.*;


public class proj1 {
 
 public static void main(String[] args) {
	DecimalFormat df = new DecimalFormat("#0.00");
	Scanner s = new Scanner(System.in);
 
	
System.out.println("  ***********     **         *      *******       *         *");                         
System.out.println("  *         *     * *        *      *      *       *       *");                         
System.out.println("  *         *     *  *       *      *       *       *     *");                           
System.out.println("  *         *     *   *      *      *        *       *   *");                          
System.out.println("  *         *     *    *     *      *        *        * *");                      
System.out.println("  ***********     *     *    *      *        *         *");                   
System.out.println("  *         *     *      *   *      *        *        *");          
System.out.println("  *         *     *       *  *      *       *        *");      
System.out.println("  *         *     *        * *      *      *        *"); 
System.out.println("  *         *     *         **      *******        *");

	System.out.print("Enter the weight of the exams (example: 55 for 55%): ");
		double examweight = Integer.parseInt(s.nextLine());
	System.out.print("Enter the weight of the projects: ");
		double projectweight = Integer.parseInt(s.nextLine());;
	System.out.print("Enter your exam average(example: 58 for 58%): ");
		double examavg = Integer.parseInt(s.nextLine());
	System.out.print("Enter your project average: ");
		double projectavg = Integer.parseInt(s.nextLine());
 
		
		double Project = projectavg * (projectweight/100);
		double Exam = examavg * (examweight/100);
		double average = (Project + Exam);
		
	System.out.println("Overall Average: " + df.format(average) + "%\n");
		
	System.out.print("How many slices of pizza?  ");
		int slices = Integer.parseInt(s.nextLine());
		int slice1 = slices/3;
		int slice2 = slices/4;
		int slice3 = slices/5;
		int leftover1 = slices%3;
		int leftover2 = slices%4;
		int leftover3 = slices%5;
	System.out.println("");
		
	System.out.println("For three people, each person can have " + slice1 + " slices with " + leftover1 + " leftover");
	System.out.println("For four people, each person can have " + slice2 + " slices with " + leftover2 + " leftover");
	System.out.println("For five people, each person can have " + slice3 + " slices with " + leftover3 + " leftover");	
	
		
		
		
		
		
		
		
		
	}
}

	