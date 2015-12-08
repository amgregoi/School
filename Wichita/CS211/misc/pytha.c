/*************************************************
*Andy Gregoire					 *
*j455z944					 *
*This progam will calculate slary mans total     *
* gross income					 *				 
*ETA - 1.5 hour               			 *	 
*Acutal time - 2 hour   			 *
**************************************************/

#include <stdio.h>

int main()
{
    int a, /*side */
        b, /*side */
        c, /*Hypotenuse */
        total = 0, /*counter; total number of triplets */
        max=500;

    for (a = 1; a <= max; a++ )
    {
        for (b =1; b <= max; b++)
	{
            for (c =1; c <= max; c++)
	    {
                if ((a * a) + (b * b) == (c * c))
                    {
                        printf("%3d, %3d, %3d\n", a,b,c);
			total++;
                    }
            }
	}
    }
    printf("A total of %d triples were found.", total);
    return 0;
}