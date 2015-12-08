/****************************************************
*Andy Gregoire                                      *
*j455z944                                           *
*This progam will calculate slary mans total        *
* gross income                                      *
*ETA - 1 hours                                      *
*Acutal time - ~45 mins                             *
****************************************************/

# include <stdio.h> /* needed to perform input & output */

int main ()
{
    int hours;
    double rate,
        Salary;
         
    /* Variable Input*/
    printf ( "Enter number of Hours Worked" );
    scanf ( "%d", &hours );
    printf ("Enter hourly rate" );
    scanf ( "%lf", &rate);
    
    if (hours <= 40){
            Salary = (hours * rate);
    }
    else{
        Salary = ((40 * rate) + ((hours - 40) * (rate * 1.5 )));
    } 
    
    /*Variable Output*/
    printf ( "Salary is %.2lf\n", Salary);
    printf( "Enter number of Hours Worked (-1 to end) ==>" );
    scanf( "%d", &hours);
    
    return 0;
}