/****************************************************
*Andy Gregoire                                      *
*j455z944                                           *
*This progam will calculate slary mans total        *
* gross income                                      *
****************************************************/

# include <stdio.h> /* needed to perform input &  output */

int main ()
{
    double Salary,
        grossSales;
	 
  
    printf ( "Enter sales in Dollars " );
    scanf ( "%lf", &grossSales);

    while ( grossSales >= 0 ){
        Salary = (200 + (grossSales * .09));
        printf ( "Salary is %.2lf\n", Salary);
        printf ( "Enter sales in Dollars (-1 to end) ==>" );
        scanf ( "%lf", &grossSales);
    }
    return 0;
}
    