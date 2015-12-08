/**********************************************
* Name: Andy Gregoire                                                  *
* Date: 2-5-2013                                               *
* Assignment: Project 1: Binary counting                         *
***********************************************
* Takes user input and counts up to it from zero in binary       *
***********************************************/
#include <stdio.h>

/* printBin - prints inputed number into binary format */
void printBin(int num)
{
        if(num <= 1)//takes care of default cases
        {
                printf("%d", num);
                return;
        }
        int remain = num % 2;//finds the remainder (1 or 0 bit of the number)
        printBin(num/2);    //recursive call of our number (shifted left 1)
        printf("%d", remain);//prints the remainder bit
}

/*Finds largest power of 2 for our inputed number */
int biggestPower(int num, int pow)
{
        if(num >= pow*2) biggestPower(num, pow*2);//recursive call to find large$
        else    return pow;     //returns largest power of 2
}

/*Main - reads user input, calls biggestPower function, and printBin function,
        to print binary format of all numbers between zero to input number */
int main()
{
        int num, i, pow;
        do{
        printf("Enter the number to count up to: ");
        scanf("%d", &num);
        }while(num <= -1);
        pow = biggestPower(num, 1);
        for(i=0; i<=num; i++)
        {
                printBin(i);
                printf("\n");
        }
//      printf("Largest Power of %d is: %d\n", num, pow);
        return 0;
}
