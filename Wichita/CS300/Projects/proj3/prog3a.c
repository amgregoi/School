/************************************************************
 *Andy Gregoire                                             *
 *j455z944                                                  *
 *Summary: Decimal to hex conversion                        *
 *  using a stack                                           *
 ************************************************************/


#include "../Stack/stackadt.h"
#include <stdio.h>
#include <stdlib.h>

int main()
{
    int *intPtr;
    int x=0;
    int base = 16;
    
    STACK *stack = createStack ();
      printf("Enter decimal number: ");
      scanf("%d", &x);
      printf("\n\n");
      
    
    if(x>=base)
    {
        intPtr = (int *) malloc(sizeof(int)); *intPtr = x/base;
      	printf("%x", *intPtr);
        push(stack, intPtr);
        x = x%base;
    }
    
    while(x<base)
    {
        intPtr = (int *) malloc(sizeof(int)); *intPtr = x;
        printf("%x \n", *intPtr);
        push(stack, intPtr);
        break;
    }
    
    printStack(stack);
    destroyStack(stack);
    
    return 0;
}
