import java.util.*;

public class Proj2 {
	public static void main(String[] args) {
		//"draw" 5 cards and print them out
		//print the classification
		Random r = new Random();
		int suit1 = r.nextInt(4)+1;
		int val1 = r.nextInt(13)+2;
		int suit2 = r.nextInt(4)+1;
		int val2 = r.nextInt(13)+2;
		int suit3 = r.nextInt(4)+1;
		int val3 = r.nextInt(13)+2;
		int suit4 = r.nextInt(4)+1;
		int val4 = r.nextInt(13)+2;
		int suit5 = r.nextInt(4)+1;
		int val5 = r.nextInt(13)+2;

		System.out.println("Your hand is: ");
		if (val1 == 14) System.out.print("\tAce");
		else if (val1 == 11) System.out.print("\tJack");
		else if (val1 == 12) System.out.print("\tQueen");
		else if (val1 == 13) System.out.print("\tKing");
		else System.out.print("\t" + val1);
		System.out.print(" of ");
		switch(suit1) {
			case 1:
				System.out.println("Spades");
				break;
			case 2:
				System.out.println("Hearts");
				break;
			case 3:
				System.out.println("Clubs");
				break;
			case 4:
				System.out.println("Diamonds");
				break;
		}

		if (val2 == 14) System.out.print("\tAce");
		else if (val2 == 11) System.out.print("\tJack");
		else if (val2 == 12) System.out.print("\tQueen");
		else if (val2 == 13) System.out.print("\tKing");
		else System.out.print("\t" + val2);
		System.out.print(" of ");
		switch(suit2) {
			case 1:
				System.out.println("Spades");
				break;
			case 2:
				System.out.println("Hearts");
				break;
			case 3:
				System.out.println("Clubs");
				break;
			case 4:
				System.out.println("Diamonds");
				break;
		}

		if (val3 == 14) System.out.print("\tAce");
		else if (val3 == 11) System.out.print("\tJack");
		else if (val3 == 12) System.out.print("\tQueen");
		else if (val3 == 13) System.out.print("\tKing");
		else System.out.print("\t" + val3);
		System.out.print(" of ");
		switch(suit3) {
			case 1:
				System.out.println("Spades");
				break;
			case 2:
				System.out.println("Hearts");
				break;
			case 3:
				System.out.println("Clubs");
				break;
			case 4:
				System.out.println("Diamonds");
				break;
		}

		if (val4 == 14) System.out.print("\tAce");
		else if (val4 == 11) System.out.print("\tJack");
		else if (val4 == 12) System.out.print("\tQueen");
		else if (val4 == 13) System.out.print("\tKing");
		else System.out.print("\t" + val4);
		System.out.print(" of ");
		switch(suit4) {
			case 1:
				System.out.println("Spades");
				break;
			case 2:
				System.out.println("Hearts");
				break;
			case 3:
				System.out.println("Clubs");
				break;
			case 4:
				System.out.println("Diamonds");
				break;
		}

		if (val5 == 14) System.out.print("\tAce");
		else if (val5 == 11) System.out.print("\tJack");
		else if (val5 == 12) System.out.print("\tQueen");
		else if (val5 == 13) System.out.print("\tKing");
		else System.out.print("\t" + val5);
		System.out.print(" of ");
		switch(suit5) {
			case 1:
				System.out.println("Spades");
				break;
			case 2:
				System.out.println("Hearts");
				break;
			case 3:
				System.out.println("Clubs");
				break;
			case 4:
				System.out.println("Diamonds");
				break;
		}

		//print whether there is a pair
		int valPair = -1;
		if (val1 == val2 || val1 == val3 || val1 == val4 || val1 == val5) {
			valPair = val1;
		}
		else if (val2 == val3 || val2 == val4 || val2 == val5) {
			valPair = val2;
		}
		else if (val3 == val4 || val3 == val5) {
			valPair = val3;
		}
		else if(val4 == val5) {
			valPair = val4;
		}
		if (valPair == -1) System.out.println("\nYou have no pairs");
		else {
			if (valPair == 14) System.out.print("\nYou have a pair of Aces");
			else if (valPair == 11) System.out.print("\nYou have a pair of Jacks");
			else if (valPair == 12) System.out.print("\nYou have a pair of Queens");
			else if (valPair == 13) System.out.print("\nYou have a pair of Kings");
			else {
				System.out.println("\nYou have a pair of " + valPair + "s");
			}
		}

		//print the highest card (Ace high)
		int valMax = -1;
		if (val1 >= val2 && val1 >= val3 && val1 >= val4 && val1 >= val5) {
			valMax = val1;
		}
		else if (val2 >= val1 && val2 >= val3 && val2 >= val4 && val2 >= val5) {
			valMax = val2;
		}
		else if (val3 >= val1 && val3 >= val2 && val3 >= val4 && val3 >= val5) {
			valMax = val3;
		}
		else if (val4 >= val1 && val4 >= val2 && val4 >= val3 && val4 >= val5) {
			valMax = val4;
		}
		else {
			valMax = val5;
		}


		System.out.print("\nYour highest card is a(n) ");
		if (valMax == 14) System.out.println("Ace");
		else if (valMax == 11) System.out.println("Jack");
		else if (valMax == 12) System.out.println("Queen");
		else if (valMax == 13) System.out.println("King");
		else {
			System.out.println(valMax);
		}
	}
}