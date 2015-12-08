/************************************************************
 *Andy Gregoire                                             *
 *j455z944                                                  *
 *Summary: Checks if a string is palindrome                 *
 ************************************************************/
#include <stdio.h>
#include <stdlib.h>

int main(int argc,char *argv[])
{
    int strLen=0, i;
    
    if(argv[1] == NULL){
        printf("Command: %s <enter string>\n", argv[0]);
        return(0);
    }
    while((argv[1][strLen])!= '\0'){
        strLen++;
    }
    for(i = 0;i < strLen/2;i++){
        if(argv[1][i] != argv[1][strLen-1-i]){
            printf("%s is Not palindrome\n",argv[1]);
            return(0);
        }
    }
    
    printf("%s is Palindrome\n",argv[1]);
    return 0;
}
