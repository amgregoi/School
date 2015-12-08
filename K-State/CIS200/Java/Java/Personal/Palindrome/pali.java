import java.io.*;

public class pali  {
  public static void main(String [] args){
  
  
  try{
	  BufferedReader object = new BufferedReader(
	  new InputStreamReader(System.in));
	  System.out.print("Enter number: ");
	  int num= Integer.parseInt(object.readLine());
	  int n = num;
	  int rev=0;
	  System.out.println("Number: ");
	  System.out.println(" "+ num);
	  
	  for (int i=0; i<=num; i++){
	  int r=num%10;
	  num=num/10;
	  rev=rev*10+r;
	  i=0;
	  }
	  
	  if(n == rev){
	  System.out.println("After reversing the number: "+ " ");
	  System.out.println(" "+ rev);
	  System.out.print("Number is palindrome!");
	  }
	  else{
	  System.out.println("Number is not palindrome!");
	  }
  }
  
  catch(Exception e){
  System.out.println("Out of range!");
  }
  }
} 