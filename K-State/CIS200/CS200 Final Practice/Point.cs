using System;
public class Point {

	private double x;
	private double y;
	
	public Point(double a, double b){
		x = a;
		y = b;
	}
	
	public void Print(){
		Console.WriteLine("("+x+","+y+")");
	}	

	
	public Point midpoint(Point z){
		double newx = (x+z.x)/2;
		double newy = (y+z.y)/2;
		
		Point result = new Point(newx, newy);
		return result;
	}
}