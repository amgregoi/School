import java.util.*;
import java.text.*;


public class fact {
 
 public static void main(String[] args) {
	Scanner s = new Scanner(System.in);
	Random r = new Random();
	
	int a = 0;
	int fact = 1;
	
	
	System.out.println("Enter number");
	a = Integer.parseInt(s.nextLine());
	
	System.out.print("Factorial of "+a+" is: ");
	for(int i=1; i<=a; i++){
		
		fact*=i;
	}
	
	System.out.println(fact);
	}
	}