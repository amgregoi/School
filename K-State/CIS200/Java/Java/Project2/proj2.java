/**
* (Playing cards)
*
* Author: (Andy Gregoire)
* Project: (Project2)
*/

import java.util.*;
import java.text.*;


public class proj2 {
 
 public static void main(String[] args) {
	Scanner s = new Scanner(System.in);
	Random r = new Random();
	
	//String str = s.nextLine();
	int card1 = 0;
	int card2 = 0;
	int card3 = 0;
	int card4 = 0;
	int card5 = 0;
	int cardx = 0;
	int twoPair= 0;
	int threeKind = 0;
	int fourKind = 0;
	int fullHouse = 0;
	int straight = 0;
	int flush = 0;
	int royalFlush = 0;
	int straightFlush = 0;
	int rfh = 0; 
		
	int suit0=0;	// diamonds  - Change value to 5 to test for flushes
	int suit1=0;	// hearts
	int suit2=0;	// clubs
	int suit3=0;	// spades
			
			/*    Used for hardcoding		
			card1 = 9;		// hardcoded numbers are 1 less than the card (i.e. 7 is hardcoded 6)
			card2 = 12;
			card3 = 3;
			card4 = 10;
			card5 = 1;
			*/
		
	//################################ Random 5 cards ################################
	for(int x=0; x<=4; x++){
		int suit = r.nextInt(4);
		int card = r.nextInt(13)+1;

	//	/*  // note out section for hardcoding
		if(card == 13){
			System.out.print( "Ace of ");
			if(x == 0){
				card1 = 13;}
				if(x == 1){
					card2 = 13;}
					if(x == 2){
						card3 = 13;}
						if (x == 3){
							card4 = 13; }
							if (x == 4){
								card5 = 13; }
		}
		if(card == 12){
			System.out.print( "King of ");
			if(x == 0){
				card1 = 12;}
				if(x == 1){
					card2 = 12;}
					if(x == 2){
						card3 = 12;}
						if (x == 3){
							card4 = 12; }
							if (x == 4){
								card5 = 12; }

		}
		if(card == 11){
			System.out.print( "Queen of ");
			if(x == 0){
				card1 = 11;}
				if(x == 1){
					card2 = 11;}
					if(x == 2){
						card3 = 11;}
						if (x == 3){
							card4 = 11; }
							if (x == 4){
								card5 = 11; }

		}
		if(card == 10){
			System.out.print( "Jack of ");
			if(x == 0){
				card1 = 10;}
				if(x == 1){
					card2 = 10;}
					if(x == 2){
						card3 = 10;}
						if (x == 3){
							card4 = 10; }
							if (x == 4){
								card5 = 10; }

		}
		if(card == 9){
			System.out.print( "10 of ");
			if(x == 0){
				card1 = 9;}
				if(x == 1){
					card2 = 9;}
					if(x == 2){
						card3 = 9;}
						if (x == 3){
							card4 = 9; }
							if (x == 4){
								card5 = 9; }
		}
		if(card == 8){
			System.out.print( "9 of ");
			if(x == 0){
				card1 = 8;}
				if(x == 1){
					card2 = 8;}
					if(x == 2){
						card3 = 8;}
						if (x == 3){
							card4 = 8; }
							if (x == 4){
								card5 = 8; }

		}
		if(card == 7){
			System.out.print( "8 of ");
			if(x == 0){
				card1 = 7;}
				if(x == 1){
					card2 = 7;}
					if(x == 2){
						card3 = 7;}
						if (x == 3){
							card4 = 7; }
							if (x == 4){
								card5 = 7; }

		}
		if(card == 6){
			System.out.print( "7 of ");
			if(x == 0){
				card1 = 6;}
				if(x == 1){
					card2 = 6;}
					if(x == 2){
						card3 = 6;}
						if (x == 3){
							card4 = 6; }
							if (x == 4){
								card5 = 6; }

		}
		if(card == 5){
			System.out.print( "6 of ");
			if(x == 0){
				card1 = 5;}
				if(x == 1){
					card2 = 5;}
					if(x == 2){
						card3 = 5;}
						if (x == 3){
							card4 = 5; }
							if (x == 4){
								card5 = 5; }

		}
		if(card == 4){
			System.out.print( "5 of ");
			if(x == 0){
				card1 = 4;}
				if(x == 1){
					card2 = 4;}
					if(x == 2){
						card3 = 4;}
						if (x == 3){
							card4 = 4; }
							if (x == 4){
								card5 = 4; }

		}
		if(card == 3){
			System.out.print( "4 of ");
			if(x == 0){
				card1 = 3;}
				if(x == 1){
					card2 = 3;}
					if(x == 2){
						card3 = 3;}
						if (x == 3){
							card4 = 3; }
							if (x == 4){
								card5 = 3; }

		}
		if(card == 2){
			System.out.print( "3 of ");
			if(x == 0){
				card1 = 2;}
				if(x == 1){
					card2 = 2;}
					if(x == 2){
						card3 = 2;}
						if (x == 3){
							card4 = 2; }
							if (x == 4){
								card5 = 2; }

		}
		if(card == 1){
			System.out.print( "2 of ");
			if(x == 0){
				card1 = 1;}
				if(x == 1){
					card2 = 1;}
					if(x == 2){
						card3 = 1;}
						if (x == 3){
							card4 = 1; }
							if (x == 4){
								card5 = 1; }
		}
		
		//################################ Set suit of card ################################
		if(suit == 0){
			System.out.println( "diamonds");
			suit0++;
		}
		if(suit == 1){
			System.out.println( "hearts");
			suit1++;
		}
		if(suit == 2){
			System.out.println( "clubs");
			suit2++;
		}
		if(suit == 3){
			System.out.println( "spades");
			suit3++;
		}
	//	*/  // End - note out section for hardcoding
	}
	
	System.out.println();
	//################################ Test for pair ################################
	if(card1 == card2){
		if(card1 == 10){
			System.out.println("You have a pair of jacks");
			}
		else if(card1 == 11){
			System.out.println("You have a pair of queens");
			}
		else if(card1 == 12){
			System.out.println("You have a pair of kings");
			}
		else if(card1 == 13){
			System.out.println("You have a pair of aces");
			}
		else if(card1 < 10){
			cardx = card1+1;
			System.out.println("You have a pair of " + cardx + "'s");
			}
		}
	else if(card1 == card3){
		if(card1 == 10){
			System.out.println("You have a pair of jacks");
			}
		else if(card1 == 11){
			System.out.println("You have a pair of queens");
			}
		else if(card1 == 12){
			System.out.println("You have a pair of kings");
			}
		else if(card1 == 13){
			System.out.println("You have a pair of aces");
			}
		else if(card1 < 10){
			cardx = card1+1;
			System.out.println("You have a pair of " + cardx + "'s");
			}
		}
	else if(card1 == card4){
		if(card1 == 10){
			System.out.println("You have a pair of jacks");
			}
		else if(card1 == 11){
			System.out.println("You have a pair of queens");
			}
		else if(card1 == 12){
			System.out.println("You have a pair of kings");
			}
		else if(card1 == 13){
			System.out.println("You have a pair of aces");
			}
		else if(card1 < 10){
			cardx = card1+1;
			System.out.println("You have a pair of " + cardx + "'s");
			}
		}
	else if(card1 == card5){
		if(card1 == 10){
			System.out.println("You have a pair of jacks");
			}
		else if(card1 == 11){
			System.out.println("You have a pair of queens");
			}
		else if(card1 == 12){
			System.out.println("You have a pair of kings");
			}
		else if(card1 == 13){
			System.out.println("You have a pair of aces");
			}
		else if(card1 < 10){
			cardx = card1+1;
			System.out.println("You have a pair of " + cardx + "'s");
			}
		}
	else if(card2 == card3){
		if(card2 == 10){
			System.out.println("You have a pair of jacks");
			}
		else if(card2 == 11){
			System.out.println("You have a pair of queens");
			}
		else if(card2 == 12){
			System.out.println("You have a pair of kings");
			}
		else if(card2 == 13){
			System.out.println("You have a pair of aces");
			}
		else if(card2 < 10){
			cardx = card2+1;
			System.out.println("You have a pair of " + cardx + "'s");
			}
		}
	else if(card2 == card4){
		if(card2 == 10){
			System.out.println("You have a pair of jacks");
			}
		else if(card2 == 11){
			System.out.println("You have a pair of queens");
			}
		else if(card2 == 12){
			System.out.println("You have a pair of kings");
			}
		else if(card2 == 13){
			System.out.println("You have a pair of aces");
			}
		else if(card2 < 10){
			cardx = card2+1;
			System.out.println("You have a pair of " + cardx + "'s");
			}
		}
	else if(card2 == card5){
		if(card2 == 10){
			System.out.println("You have a pair of jacks");
			}
		else if(card2 == 11){
			System.out.println("You have a pair of queens");
			}
		else if(card2 == 12){
			System.out.println("You have a pair of kings");
			}
		else if(card2 == 13){
			System.out.println("You have a pair of aces");
			}
		else if(card2 < 10){
			cardx = card2+1;
			System.out.println("You have a pair of " + cardx + "'s");
			}
		}
	else if(card3 == card4){
		if(card3 == 10){
			System.out.println("You have a pair of jacks");
			}
		else if(card3 == 11){
			System.out.println("You have a pair of queens");
			}
		else if(card3 == 12){
			System.out.println("You have a pair of kings");
			}
		else if(card3 == 13){
			System.out.println("You have a pair of aces");
			}
		else if(card3 < 10){
			cardx = card3+1;
			System.out.println("You have a pair of " + cardx + "'s");
		}
		}
	else if(card3 == card5){
		if(card3 == 10){
			System.out.println("You have a pair of jacks");
			}
		else if(card3 == 11){
			System.out.println("You have a pair of queens");
			}
		else if(card3 == 12){
			System.out.println("You have a pair of kings");
			}
		else if(card3 == 13){
			System.out.println("You have a pair of aces");
			}
		else if(card3 < 10){
			cardx = card3+1;
			System.out.println("You have a pair of " + cardx + "'s");
		}
		}
	else if(card4 == card5){
		if(card4 == 10){
			System.out.println("You have a pair of jacks");
			}
		else if(card4 == 11){
			System.out.println("You have a pair of queens");
			}
		else if(card4 == 12){
			System.out.println("You have a pair of kings");
			}
		else if(card4 == 13){
			System.out.println("You have a pair of aces");
			}
		else if(card4 < 10){
			cardx = card4+1;
			System.out.println("You have a pair of " + cardx + "'s");
		}
		}
	else{
		// no pairs
		System.out.println("you have no pairs");
		}
		
	//################################ Highest Card ################################
	
	if(card1 >= card2 && card1 >= card3 && card1 >= card4 && card1 >= card5){
		System.out.print("Your highest card is a(n): " );
		if(card1 == 10){
			System.out.println("jack");
			}
		else if(card1 == 11){
			System.out.println("queen");
			}
		else if(card1 == 12){
			System.out.println("king");
			}
		else if(card1 == 13){
			System.out.println("ace");
			}
		else if(card1 < 10){
			cardx = card1+1;
			System.out.println(cardx);
		}
	}
	else if(card2 >= card3 && card2 >= card4 && card2 >= card5){
		System.out.print("Your highest card is a(n): " );
		if(card2 == 10){
			System.out.println("jack");
			}
		else if(card2 == 11){
			System.out.println("queen");
			}
		else if(card2 == 12){
			System.out.println("king");
			}
		else if(card2 == 13){
			System.out.println("ace");
			}
		else if(card2 < 10){
			cardx = card2+1;
			System.out.println(cardx);
		}
	}
	else if(card3 >= card4 && card3 >= card5){
		System.out.print("Your highest card is a(n): " );
		if(card3 == 10){
			System.out.println("jack");
			}
		else if(card3 == 11){
			System.out.println("queen");
			}
		else if(card3 == 12){
			System.out.println("king");
			}
		else if(card3 == 13){
			System.out.println("ace");
			}
		else if(card3 < 10){
			cardx = card3+1;
			System.out.println(cardx);
		}
	}
	else if(card4 >= card5){
		System.out.print("Your highest card is a(n): " );
		if(card4 == 10){
			System.out.println("jack");
			}
		else if(card4 == 11){
			System.out.println("queen");
			}
		else if(card4 == 12){
			System.out.println("king");
			}
		else if(card4 == 13){
			System.out.println("ace");
			}
		else if(card4 < 10){
			cardx = card4+1;
			System.out.println(cardx);
		}
	}
	else{
		System.out.print("Your highest card is a(n): " );
		if(card5 == 10){
			System.out.println("jack");
			}
		else if(card5 == 11){
			System.out.println("queen");
			}
		else if(card5 == 12){
			System.out.println("king");
			}
		else if(card5 == 13){
			System.out.println("ace");
			}
		else if(card5 < 10){
			cardx = card5+1;
			System.out.println(cardx);
		}
	}
	
	System.out.println();
	//################################ Extra credit ################################
	
	//################################ two pair ################################
	if(card1 == card2){
		twoPair++;
		}
	else if(card1 == card3){
		twoPair++;
		}
	else if(card1 == card4){
		twoPair++;
		}
	else if(card1 == card5){
		twoPair++;
		}
	if(card2 == card3){
		twoPair++;
		}
	else if(card2 == card4){
		twoPair++;
		}
	else if(card2 == card5){
		twoPair++;
		}
	if (card3 == card4){
		twoPair++;
		}
	else if (card3 == card5){
		twoPair++;
		}	
	if (card4 == card5){
		twoPair++;
		}
		
		
	//################################ Three of a Kind ################################
	if(card1 == card2){
		threeKind++;
		}
	if(card1 == card3){
		threeKind++;
		}
	if(card1 == card4){
		threeKind++;
		}
	if(card1 == card5){
		threeKind++;
		}
	if(card2 == card3){
		threeKind++;
		}
	if(card2 == card4){
		threeKind++;
		}
	if(card2 == card5){
		threeKind++;
		}
	if (card3 == card4){
		threeKind++;
		}
	if (card3 == card5){
		threeKind++;
		}	
	if (card4 == card5){
		threeKind++;
		}
	
	//################################# Straight #################################
	if(card1 < card2 && card1 < card3 && card1 < card4 && card1 < card5){
		if(card1 == 9){
			rfh = 1;
		}
		cardx = card1;
		cardx++;
		if(cardx == card2 ||cardx == card3 ||cardx == card4 ||cardx == card5){
			cardx++;
			if(cardx == card2 ||cardx == card3 ||cardx == card4 ||cardx == card5){
				cardx++;
				if(cardx == card2 ||cardx == card3 ||cardx == card4 ||cardx == card5){
					cardx++;
					if(cardx == card2 ||cardx == card3 ||cardx == card4 ||cardx == card5){
						straight = 1;
						//System.out.println("You have a Straight"); // -test
						
					}
				}
			}
		}
	}
	if(card2 < card1 && card2 < card3 && card2 < card4 && card2 < card5){
		if(card2 == 9){
			rfh = 1;
		}
		cardx = card2;
		cardx++;
		if(cardx == card1 ||cardx == card3 ||cardx == card4 ||cardx == card5){
			cardx++;
			if(cardx == card1 ||cardx == card3 ||cardx == card4 ||cardx == card5){
				cardx++;
				if(cardx == card1 ||cardx == card3 ||cardx == card4 ||cardx == card5){
					cardx++;
					if(cardx == card1 ||cardx == card3 ||cardx == card4 ||cardx == card5){
						straight = 1;
						//System.out.println("You have a Straight"); // -test
						
					}
				}
			}
		}
	}
	if(card3 < card2 && card3 < card1 && card3 < card4 && card3 < card5){
		if(card3 == 9){
			rfh = 1;
		}
		cardx = card3;
		cardx++;
		if(cardx == card2 ||cardx == card1 ||cardx == card4 ||cardx == card5){
			cardx++;
			if(cardx == card2 ||cardx == card1 ||cardx == card4 ||cardx == card5){
				cardx++;
				if(cardx == card2 ||cardx == card1 ||cardx == card4 ||cardx == card5){
					cardx++;
					if(cardx == card2 ||cardx == card1 ||cardx == card4 ||cardx == card5){
						straight = 1;
						//System.out.println("You have a Straight"); // -test
						
					}
				}
			}
		}
	}
	if(card4 < card2 && card4 < card3 && card4 < card1 && card4 < card5){
		if(card4 == 9){
			rfh = 1;
		}
		cardx = card4;
		cardx++;
		if(cardx == card2 ||cardx == card3 ||cardx == card1 ||cardx == card5){
			cardx++;
			if(cardx == card2 ||cardx == card3 ||cardx == card1 ||cardx == card5){
				cardx++;
				if(cardx == card2 ||cardx == card3 ||cardx == card1 ||cardx == card5){
					cardx++;
					if(cardx == card2 ||cardx == card3 ||cardx == card1 ||cardx == card5){
						straight = 1;
						//System.out.println("You have a Straight"); // -test
						
					}
				}
			}
		}
	}
	if(card5 < card2 && card5 < card3 && card5 < card4 && card5 < card1){
		if(card5 == 9){
			rfh = 1;
		}
		cardx = card5;
		cardx++;
		if(cardx == card2 ||cardx == card3 ||cardx == card4 ||cardx == card1){
			cardx++;
			if(cardx == card2 ||cardx == card3 ||cardx == card4 ||cardx == card1){
				cardx++;
				if(cardx == card2 ||cardx == card3 ||cardx == card4 ||cardx == card1){
					cardx++;
					if(cardx == card2 ||cardx == card3 ||cardx == card4 ||cardx == card1){
						straight = 1;
						//System.out.println("You have a Straight"); // -test
						
					}
				}
			}
		}
	}

	//################################# Flush ######################################
	//System.out.println("Dimaonds: " + suit0 + " hearts: " + suit1 + " clubs: " + suit2 + " spades: " + suit3);
	if(suit0 == 5 || suit1 == 5 || suit2 == 5 || suit3 == 5){
		flush = 1;
		//System.out.println("You have a Flush"); // -test
	}
	//################################# Full House #################################
	if(threeKind > 3 && twoPair >= 1){
		fullHouse = 1;
		//System.out.println("threeKind: " + threeKind +" twoPair: " + twoPair); // -test
	}
	
	//################################# Four of a Kind #################################
	if(threeKind == 6){
		fourKind = 1;
		//System.out.println("four of a kind"); // -test
	}
	
	//################################# Straight Flush #################################
	if(straight == 1 && flush == 1){
		straightFlush = 1;
		//System.out.println("Straight Flush"); // -test
	}
	
	//################################# Royal Flush #################################
	if(straight == 1 && flush == 1 && rfh == 1){
		royalFlush = 1;
		//System.out.println("Royal Flush"); // -test
	}

	//################################# Print Statements #################################
	
	if(royalFlush == 1){
		System.out.println("You have a Royal Flush");
	}
	else if(straightFlush == 1){
		System.out.println("You have a Straight Flush");
	}
	else if(fourKind == 1){
		System.out.println("You have Four of a Kind");
	}
	else if(fullHouse == 1){
		System.out.println("You have a Full House");
	}
	else if(flush == 1){
		System.out.println("You have a Flush");
	}
	else if(straight == 1){
		System.out.println("You have a Straight");
	}
	else if(threeKind >= 3){
		System.out.println("You have Three of a Kind");
	}
	else if(twoPair == 2){
		System.out.println("You have Two Pairs");
	}
	else if(twoPair == 1){
		System.out.println("You have a Pair");
	}
	else{
		System.out.println("You have High Card");
	}
}
}
	