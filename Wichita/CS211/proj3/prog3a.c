/****************************************************
*Andy Gregoire                                      *
*j455z944                                           *
*This program will determine if a department        *
*store customer has exceeded the credit limit on    *
*acharge account                                    *
****************************************************/

# include <stdio.h> /* needed to perform input &    output */

int main ()
{
    int accountNumber;
    double beginBalance,
	 totalCharges,
	 totalCredits,
	 newBalance,
	 creditLimit;
	 
    printf( "Enter Account number " );
    scanf( "%d", &accountNumber );
    
    
    while (accountNumber >= 0 ){
        printf ( "Enter    Beginning Balance " );
        scanf ( "%lf", &beginBalance );
    
        printf( "Enter Total Charges " );
        scanf ( "%.2lf", &totalCharges );
    
        printf( "Enter Total Credits " );
        scanf ( "%.2lf", &totalCredits );
    
        printf( "Enter Credit Limit " );
        scanf ( "%.2lf", &creditLimit );
    
        newBalance = ((beginBalance + totalCharges) - totalCredits);
     
        if (newBalance > creditLimit){
                printf ( "Account: %d\n", accountNumber );
                printf ( "Credit Limit: %lf\n", creditLimit );
                printf ( "Balance: %lf\n", newBalance );
                printf ( "Credit Limit    Exceeded\n" );
        }
            
        printf( "please enter the Account Number (-1 to end) ==>" );
        scanf( "%d", &accountNumber);
    }

        
    return 0;
}
    
    
    
	 