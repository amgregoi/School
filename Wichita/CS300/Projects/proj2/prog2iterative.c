/************************************************************
 *Andy Gregoire                                             *
 *j455z944                                                  *
 *Summary: Checks if string is palindrome (iterative)       *
 ************************************************************/
#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
#include<string.h>

int Palindrome();

int main ()
{
    int i = 0;
    int p,q=0;
    int ch;
    char str[100];

    printf("Enter String (max 100 chars): ");

    while ((ch = getchar()) != '\n'){
        /*tests the string for spaces and punctuation and gets rid of them*/
        if (isalnum(ch)) {
            str[i] = ch;
            i++;
        }  
    }

    /* Ends the string */
    str[i] = '\0';


    /*Tests whether entered string is Palindrome*/
    for(p=(i-1);p>=q;p--){
        if(str[p] != str[q]){
            printf("%s: is not palindrome.\n", str);
            exit(0);
        }
        q++;
    }
    
    printf("string length is %d\n", i);
    printf("%s: is Palindrome\n", str);

   
}