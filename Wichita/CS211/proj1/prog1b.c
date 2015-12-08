/************************************************************
 *Andy Gregoire                                             *
 *j455z944                                                  *
 *Summary: Converts inputed farenheit temperature to        *
 *degrees celsius                                           *
 ************************************************************/
#include <stdio.h>
#include <stdlib.h>

int main()
{
    double f = 32, c;
    
    while(f < 200){
        printf("Input temperature in degrees Farenheit (200+ to exit): ");
        scanf("%lf", &f);

        c=((f-32)*(5.0/9.0));
        printf("Temperatures in degrees Celsius is %.2lf\n\n", c);
    }

    exit(0);
}
