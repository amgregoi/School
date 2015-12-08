/**
* (Pig Part1)
*
* Author: (Andy Gregoire)
* Project: (Project3p1)
*Strategy: Keep rolling untill your turn total is >= 13 or you've rolled 4 times, if any
*of the previous conditions are met stop rolling.  This keeps your score greater than half way
* to goal without risking the chance of rolling 1 or if you do roll 1 before hitting 13 your not
*losing much.
*
*
*/

import java.util.*;
import java.text.*;


public class Proj3Part3 {
 
 public static void main(String[] args) {
	DecimalFormat df = new DecimalFormat("#0.00");
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
	int count1 =0;
	int count2 =0;
	int roll1 = 0;
	int roll2 = 0;
	int test = 20; // can change for different game ending numbers
	
	while(p1os < test && p2os < test){
		p1opt = 'r';
		p2opt = 'r';
		while(p1opt == 'r' && p2win == 0){
			if(p1tt < 13 || count1 <= 4){
				p1opt = 'r';
			}
			else if(p1tt > 13 || p1tt >=test){
				p1opt = 's';
			}
			if(p1opt == 'r'){
				roll = r.nextInt(6)+1;
				System.out.println("Computer1 rolled: " + roll);
				if(roll > 1){
					p1tt +=roll;
					}
				else if(roll == 1){
					p1tt = 0;
					p1opt = 'n';
					System.out.println("Turn Over.");
					count1=0;
				}
				}
			 else if( p1opt == 's'){
				p1os += p1tt;
				p1tt = 0;
				System.out.println("Turn Over.");
				count1=0;
			}
			if(p1os >= test){
				p1win = 1;
				System.out.println("Computer1 is the winner!");
			}
			
			count1++;
			
		}
		roll1++;
		while(p2opt =='r' && p1win == 0){
			if(p2tt < 13 || count2 <= 4){
				p2opt = 'r';
			}
			else if (p2tt > 13 || p2tt >= test){
				p2opt = 's';
			}
			if(p2opt == 'r'){
				roll = r.nextInt(6)+1;
				System.out.println("Computer2 rolled: " + roll);
				if(roll > 1){
					p2tt +=roll;
					}
				else if(roll == 1){
					p2tt = 0;
					System.out.println("Turn Over.");
					p2opt = 's';
					count2 = 0;
				}
				}
			else if( p2opt == 's'){
				p2os += p2tt;
				p2tt = 0;
				count2 = 0;
				System.out.println("Turn Over.");
			}
			if(p2os >= test){
				p2win = 1;
				System.out.println("Computer2 is the winner!");
			}
			count2++;
			
		}
			roll2++;
		if(p1win != 1 && p2win != 1){
			System.out.println("Current Score: Computer1 has " + p1os + ", Computer2 has " + p2os);
			}
		else{}
		}
		System.out.println();
		System.out.println("Current Score: Player 1 has " + p1os + ", Player 2 has " + p2os );
		System.out.println("Computer1 had " + roll1 +" turns" + ", Computer2 had " + roll2 + " turns");
		
		System.out.println("My calculations show an average of 3 roles to reach 20+ points");
	
	
	
	
	
	
}
}