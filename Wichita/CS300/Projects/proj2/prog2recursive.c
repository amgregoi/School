/************************************************************
 *Andy Gregoire                                             *
 *j455z944                                                  *
 *Summary: Checks if string is palindrome (recursive)       *
 ************************************************************/
#include<stdio.h>
#include<ctype.h>
#include<string.h>

int Palindrome(char *str, int index);

int main ()
{
    int i = 0;
    int ch;
    char str[100];

    printf("Enter String: ");

    while ((ch = getchar()) != '\n'){
        /*tests the string for spaces and punctuation and gets rid of them*/
        if (isalnum(ch)) {
            str[i] = ch;
            i++;
        }  
    }
    str[i] = '\0';

   
   
   
    printf("string length is %d\n", i);
    /*prints appropriate response based on what the function "Palindrome" finds */
    if ( Palindrome(str, 0) == 1)
        printf("%s is Palindrome\n", str);
    else
        printf("%s is not palindrome.\n", str);
    
    return 0;
}
   
/*Tests whether entered string is Palindrome*/
int Palindrome(char *str, int index)
{
    int i = strlen(str)-1-index;
   
    if(str[index] != str[i])
        return 0;
    if(	index >= i)
        return 1;
    else
        return Palindrome(str, index+1);
}