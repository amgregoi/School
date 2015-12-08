/**
* (Word Jumble game)
*  Note: If you un-note line 79, it will print out the jumbled word for easy checking
* Author: (Andy Gregoire)
* Project: (Project4)
*/
import java.util.*;
import java.io.*;
public class proj4 {
	public static void main(String[] args) throws IOException{
	// #####################################
		Scanner s = new Scanner(System.in);
		Random r = new Random();
		Scanner inFile = new Scanner(new File("words.txt"));
		String line = inFile.nextLine();
		String[] pieces = new String[5049];
		int i = 0;
		char choice = 'g';
		int total = 0;
		
		
		// #####################################
		
		// split file into pieces array
		while (inFile.hasNext()) {
		StringTokenizer str = new StringTokenizer(line, " ");
				line = inFile.nextLine();
				//pieces[i] = line.split(" ");
				pieces[i] = str.nextToken();
				i++;
				}
		inFile.close();
		
		do {
		choice = 'g';
		int points = 10;
		// #####################################
		String word = pieces[r.nextInt(i)];
		String[] words = word.split("");
		String[] test = new String[word.length()];
		int b = 1;
		for(int a = 0; a < word.length(); a++){
			test[a] = words[b];	
			b++;
		}
		boolean[] used = new boolean[word.length()];
		String[] newpieces = new String[word.length()];
		
		// #####################################
		
		//First Print Line
		
		
		// jumble word
		for(int k = 0; k<word.length(); k++){
			int rand = r.nextInt(word.length());
			if( used[rand] == false){
				used[rand] = true;
				newpieces[k] = test[rand];
				//System.out.print(rand);
				//System.out.print(newpieces[k]);
			}
			else
				k--;
		}
		
		while(choice == 'g' || choice == 'h'){
			System.out.print("Current puzzle: ");
			for(int c=0;c<word.length();c++){
				System.out.print(newpieces[c]);
			}
			System.out.println();		
			System.out.println("Current points for word: " + points);
			System.out.print("Enter (g)uess, (n)ew word, (h)int, or (q)uit: ");
			choice = s.nextLine().charAt(0);
			//System.out.println(choice);
			System.out.println();
			//##################  Tells word for quick testing ###################
			//System.out.println("word is: " +word);
			System.out.println();

			if(choice == 'g' || choice == 'G'){
				System.out.print("Enter your guess: ");
				String guess = s.nextLine();
				System.out.println();
				if(guess.equals(word)){
					total+=points;
					System.out.println("You guessed it!");
					System.out.println("Score for word: "+points);
					System.out.println("Total score: "+total);
					System.out.println();
					break;
				}
				else{
					if(points > 0)
						points--;
						continue;
				}				
			}
			else if(choice == 'h' || choice == 'H'){
				int rand2 = r.nextInt(word.length());
				int x = rand2+1;
				System.out.println("The letter at spot " + x + " is " + test[rand2]);
				System.out.println();
				points/=2;
				
			}
			else if(choice == 'n' || choice == 'N'){
				break;
			}
			else if(choice == 'q' || choice == 'Q'){
				break;
			}
			else{
				choice = 'g';
				System.out.println("Not an optiong try again");
				System.out.println();
			}	
		}
				
		
	}while(choice != 'q');
	System.out.println();
	System.out.println("Goodbye!");
	System.out.println("your final score is: " + total);
	}
}
