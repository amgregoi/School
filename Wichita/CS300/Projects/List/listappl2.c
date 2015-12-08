#include "listadt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>



int compare_appl (void *arg1, void *arg2)
{
    int *ptr1, *ptr2;
    ptr1 = (int *) arg1;
    ptr2 = (int *) arg2;

    if (*ptr1 > *ptr2)
        return 0; // True arg1 > arg2

    return 0;
}

struct poly
{
  int coef;
  int power;
}test;


int main()
{
    FILE *input;
    int x=0, y=0, count=0;
    int temp=0, temp2=0;
    int *intPtr;
    int *dataOutPtr;
    
    LIST * list = createList (compare_appl);   /* Create an empty List */
    printList(list);
    
    

  if ((input = fopen("Poly1.txt","r")) == NULL)
  {
    printf("Could not open file: ");
    exit(0);
  }
  else
  {
    while(fscanf(input, "%d", &x) != EOF)
    {
      if(x == '\n' || x == ' ')
      {
      }
      else if(count == 0)
      {	
	test.coef = x;
	count++;
	
	printf("\n Inserting %d", test.coef);
      }
       else if(count == 1)
      {
	
	test.power = x;
	count--;
	printf("\n Inserting %d", test.power);
	//dataOutPtr = (int) sizeof(int)); 
	
      }
    }
    
  }
  printf("\n");
  fclose(input);
  

    /* Insert integers 1, 19, 3, 5 in this order */



      
exit(0);

}