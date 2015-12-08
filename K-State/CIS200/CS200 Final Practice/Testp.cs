using System;	
public class Testp{
	public static void Main(){
		Point[] parr = new Point[10];
		
		for(int i=0; i<10;i++){
			Console.Write("Enter x value: ");
			double x = Convert.ToDouble(Console.ReadLine());
			Console.Write("Enter y value: ");
			double y = Convert.ToDouble(Console.ReadLine());
			parr[i] = new Point(x,y);
		}
		
		parr[0].Print();
		Point p = parr[1].midpoint(parr[9]);
		p.Print();
	}
}