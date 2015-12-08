#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <signal.h>


void signalHandle(int sig);     //handles floating point expection signal
int fMultiple(int x, int y);    //tests if x is a multiple of y

int main()
{
    signal(SIGFPE, signalHandle);
    int x = 20,
        y = 4;
  
   //should expect a "true"
    printf("It is %s that %d is a multiple of %d\n",
    fMultiple(x,y)?"true":"false", x, y);

    x = 19;
    y = 7;

    //Should expect a "false"
    printf("It is %s that %d is a multiple of %d\n", 
    fMultiple(x,y)?"true":"false", x, y);

    x = -42;
    y = 2;

    //Should expect a "true"
    printf("It is %s that %d is a multiple of %d\n",
    fMultiple(x,y)?"true":"false", x, y);

    x = 0;
    y = 12;

    //Should expect a true
    printf("It is %s that %d is a multiple of %d\n",
    fMultiple(x,y)?"true":"false", x, y);
    x = 12;
    y = 0;

    //Should catch division by zero (SIGFPE signal) and exit program
    printf("It is %s that %d is a multiple of %d\n", 
    fMultiple(x,y)?"true":"false", x, y);

 
     exit(0);
}


void signalHandle(int sig){
    printf("Signal caught\n");
    printf("You cannot divide by 0\n");
    printf("Program ending\n");
    
    exit(1);
}

int fMultiple(int x, int y){

    if(x % y == 0) return 1;
    return 0;
}
