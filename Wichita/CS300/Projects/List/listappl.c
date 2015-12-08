#include "listadt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int addition(LIST *list, LIST *list2);

int compare_appl (void *arg1, void *arg2)
{
    int *ptr1, *ptr2;
    ptr1 = (int *) arg1;
    ptr2 = (int *) arg2;

    if (*ptr1 > *ptr2)
        return 0; // True arg1 > arg2

    return 0;
}

int main()
{
    FILE *input;
    int x=0, count=0;
    test *ptr;
    
    LIST * list = createList (compare_appl);   /* Create an empty List */

    
    

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
	ptr = (test *) malloc(sizeof(test));
	ptr->coef = x;
	count++;
	
	//printf("\n Inserting %d to coef", ptr->coef);
      }
       else if(count == 1)
      {
	ptr->power = x;
	count--;
	insert_node(list, ptr);
      }
    }
    
  }
      fclose(input);
      printList(list);
       
      LIST * list2 = createList (compare_appl); 
      
    
      printf("\n\nPoly2\n\n");
 

  if ((input = fopen("Poly2.txt","r")) == NULL)
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
	ptr = (test *) malloc(sizeof(test));
	ptr->coef = x;
	count++;
      }
       else if(count == 1)
      {
	ptr->power = x;
	count--;
	insert_node(list2, ptr);;
      }
    }
    
  }
  fclose(input);
  printList(list2);
  addition(list, list2);=
  
exit(0);

}
