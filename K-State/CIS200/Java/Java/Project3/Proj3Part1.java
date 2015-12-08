/**
* (Pig Part1)
*
* Author: (Andy Gregoire)
* Project: (Project3p1)
*/

import java.util.*;


public class Proj3Part1 {
 
 public static void main(String[] args) {

	Scanner s = new Scanner(System.in);
	Random r = new Random();
	
	int p1os=0;
	int p2os=0;
	int p1tt=0;
	int p2tt=0;
	int roll=0;
	int rollCount=0;
	char p2opt = 'r';
	char p1opt = 'r';
	int p1win = 0;
	int p2win = 0;
	int roll1 = 0;
	int roll2 = 0;
	
	
	while(p1os < 20 && p2os < 20){
		p1opt = 'r';
		p2opt = 'r';
		while(p1opt == 'r' && p2win == 0){
			System.out.print("Player 1 turn total is " + p1tt + ". Enter (r)oll or (s)top: ");
			p1opt = (s.nextLine()).charAt(0);
			if(p1opt == 'r'){
				roll = r.nextInt(6)+1;
				System.out.println("you rolled: " + roll);
				if(roll > 1){
					p1tt +=roll;
					}
				else if(roll == 1){
					p1tt = 0;
					System.out.println("You rolled a 1 your turn total is now p1tt");
					p1opt = 'n';
				}
				}
			 else if( p1opt == 's'){
				p1os += p1tt;
				p1tt = 0;
			}
			if(p1os >= 20){
				p1win = 1;
				System.out.println("Player 1 is the winner!");
			}
			
			
		}
		roll1++;
		
		while(p2opt =='r' && p1win == 0){
			System.out.print("Player 2 turn total is " + p2tt + ". Enter (r)oll or (s)top: ");
			p2opt = (s.nextLine()).charAt(0); 
			if(p2opt == 'r'){
				roll = r.nextInt(6)+1;
				System.out.println("you rolled: " + roll);
				if(roll > 1){
					p2tt +=roll;
					}
				else if(roll == 1){
					p2tt = 0;
					System.out.println("You rolled a one your turn total is now p2tt");
					p2opt = 's';
				}
				}
			else if( p2opt == 's'){
				p2os += p2tt;
				p2tt = 0;
			}
			if(p2os >= 20){
				p2win = 1;
				System.out.println("Player 2 is the winner!");
			}
			
		}
		roll2++;
		if(p1win != 1 && p2win != 1){
				System.out.println("Current Score: Computer1 has " + p1os + ", Computer2 has " + p2os);
				}
			else{}
		}
		System.out.println();
		System.out.println("Current Score: Player 1 has " + p1os + ", Player 2 has " + p2os );
		System.out.println("Player 1 had " + roll1 +" turns" + ", Computer1 had " + roll2 + " turns");
		
	
	
	
	
	
}
}