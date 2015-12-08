/************************************************************
 *Andy Gregoire                                             *
 *j455z944                                                  *
 *Summary: postfix calculator using stack                   *
 ************************************************************/


#include "Stack/stackadt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

void doOperation(STACK *stack, char op, int first);

int main()
{
    int i, firstOperation = 1;
    char *charPtr;
    char array[50];
    
    STACK *stack = createStack ();
    
    printf("Enter postfix expression: ");
    fgets(array, 50, stdin);
    
    for(i=0; array[i] != '\n'; i++)
    {
        charPtr = (char *) malloc(sizeof((char) + 10));
        *charPtr = array[i];
        
        if(!isalpha((int)*charPtr)){
            doOperation(stack, *charPtr, firstOperation);
            firstOperation = 0;
        }
        else
            push(stack, charPtr);
    }
    
    NODE *tmp = stack->top;
    printf("\nFinal Value =  %d \n", *(int *)tmp->dataPtr);
    
    // Destroying Stack
    destroyStack(stack);
    exit(0);
}

void doOperation(STACK *stack, char op, int first)
{
    char* result = (char*) malloc(sizeof(char) + 10);
    int *temp1, *temp2, num1, num2;
    
    
    temp1 = popStack(stack);
    if(first){
        printf("Enter Value for %c: ", *temp1);
        scanf("%d", &num1);
    }
    else{
        num1 = *temp1;
    }
    
    temp2 = popStack(stack);
    printf("Enter Value for %c: ", *temp2);
    scanf("%d", &num2);
    
    if(op == '+') *result = num1+num2;
    else if(op == '-') *result = num1-num2;
    else if(op == '/') *result = num1/num2;
    else if(op == '*') *result = num1*num2;
    
    //printf("\tPushing sum: %d\n", *result);
    push(stack, result);
}












