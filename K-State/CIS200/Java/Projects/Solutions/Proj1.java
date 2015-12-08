/**
 * Proj 1 prints a snake, calculates a percent off sale, and finds change.
 *
 * @author Julie Thornton
 * @version Project 1
 */

import java.util.*;
import java.text.*;

public class Proj1 {
	public static void main(String[] args) {
		Scanner s = new Scanner(System.in);
		DecimalFormat df = new DecimalFormat("#0.00");

		//print first name
		System.out.println("       *  *     *  *       *  *****");
		System.out.println("       *  *     *  *       *  *");
		System.out.println("       *  *     *  *       *  *");
		System.out.println("       *  *     *  *       *  *");
		System.out.println("       *  *     *  *       *  *****");
		System.out.println("       *  *     *  *       *  *");
		System.out.println("       *  *     *  *       *  *");
		System.out.println(" *     *  *     *  *       *  *");
		System.out.println("  *   *    *   *   *       *  *");
		System.out.println("   ***      ***    ******  *  *****");

		//get weight of exams, exam average, weight of projects, project average
		//calculate overall score
		System.out.print("\nEnter the weight of the exams (e.g., 55 for 55%): ");
		double examWeight = Double.parseDouble(s.nextLine());
		System.out.print("Enter the weight of the projects: ");
		double projWeight = Double.parseDouble(s.nextLine());
		System.out.print("Enter your exam average (e.g., 78 for 78%): ");
		double examAvg = Double.parseDouble(s.nextLine());
		System.out.print("Enter your project average: ");
		double projAvg = Double.parseDouble(s.nextLine());

		double avg = (examWeight/100)*examAvg + (projWeight/100)*projAvg;
		System.out.println("\nOverall average: " + df.format(avg) + "%");


		//divide up pizza
		System.out.print("\nHow many slices of pizza? ");
		int slices = Integer.parseInt(s.nextLine());

		//calculate for three people
		int each = slices / 3;
		int leftover = slices % 3;
		System.out.println("\nFor three people, each person can have " + each +
							" slices with " + leftover + " leftover");

		//calculate for four people
		each = slices / 4;
		leftover = slices % 4;
		System.out.println("For four people, each person can have " + each +
							" slices with " + leftover + " leftover");

		//calculate for five people
		each = slices / 5;
		leftover = slices % 5;
		System.out.println("For five people, each person can have " + each +
							" slices with " + leftover + " leftover");
	}
}