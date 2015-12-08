import java.util.*;

public class Test {
	public static void main(String[] args){  // {"apple", "banana", "avocado", "carrot"}
		String[] word = {"apple","banana","avocado","carrot"};	
		Dictionary d = new Dictionary(word);
		
		int x = d.startsWith('a');
		System.out.println("starts with 'a': "+ x);
	
	}	
}