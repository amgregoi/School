import java.util.*;
import java.io.*;

public class Proj4 {
	public static void main(String[] args) throws IOException {
		Scanner s = new Scanner(System.in);

		//read in file of all words
		String[] words;
		Scanner inFile = new Scanner(new File("words.txt"));

		words = new String[Integer.parseInt(inFile.nextLine())];
		for (int i = 0; i < words.length; i++) {
			words[i] = inFile.nextLine();
		}
		inFile.close();

		Random r = new Random();

		//keep score
		int totalScore = 0;
		int wordScore = 10;

		char option = 'n';
		String correct = "";
		String jumble = "";

		do {
			//repeatedly let the user guess, pick a new word, or get a hint
			if (option != 'n' && option != 'N') {
				System.out.println("Current puzzle: " + jumble);
				System.out.println("Current points for word: " + wordScore);
				System.out.print("Enter (g)uess, (n)ew word, (h)int, or (q)uit: ");
				option = (s.nextLine()).charAt(0);
			}

			switch (option) {
				case 'G': case 'g':
					System.out.print("\nEnter your guess: ");
					String guess = s.nextLine();
					if (guess.toUpperCase().equals(correct.toUpperCase())) {
						System.out.println("You guessed it!");
						option = 'n';
						totalScore += wordScore;
						System.out.println("Score for word: " + wordScore);
						System.out.println("Total score: " + totalScore);
					}
					else {
						System.out.println("Nope, sorry.\n");
						if (wordScore > 0) wordScore--;
					}
					break;
				case 'N': case 'n':
					//pick a random word
					int index = r.nextInt(words.length);
					correct = words[index];
					wordScore = 10;

					//randomly jumble it
					boolean[] used = new boolean[correct.length()];
					jumble = "";

					int count = 0;
					while (count < used.length)
					{
						int pos = r.nextInt(used.length);
						if (used[pos] == false)
						{
							jumble += correct.charAt(pos);
							used[pos] = true;
							count++;
						}
					}
					System.out.println();

					option = 'g';
					break;
				case 'H': case 'h':
					index = r.nextInt(correct.length());
					char letter = correct.charAt(index);
					System.out.println("\nThe letter at spot " + (index+1) + " is " + letter + "\n");
					if (wordScore > 0) wordScore/=2;
					break;
				case 'Q': case 'q':
					System.out.println("\nGoodbye!");
					System.out.println("Final score: " + totalScore);
					break;
				default:
					System.out.println("Invalid option.\n");
			}
		} while (option != 'q' && option != 'Q');
	}
}