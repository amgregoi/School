#include "listadt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* Our Application implements a list of sorted integers with no duplicate */

/* Returns true if arg1 is greater; false otherwise */
int compare_appl (void *arg1, void *arg2)
{
    int *ptr1, *ptr2;
    ptr1 = (int *) arg1;
    ptr2 = (int *) arg2;

//    printf("\n comparing %d and %d, result = %d\n", *ptr1, *ptr2, (*ptr1 > *ptr2));
    if (*ptr1 < *ptr2)
	return 0; // True arg1 > arg2

    return 0;
}

main()
{
    FILE *input;
    int x=0, i=0;
    char a[100];
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
  while(fgets(a,2,input))
    fputs(a, stdout);

    for(i=0;i<strlen(a)-1;i++)
    {
      x = a[i];
      printf("%c\n", x);
	
    }
    a[i] = '\0';
  }
  printf("\n");
  fclose(input)
  
  

 
    


    /* Insert integers 1, 19, 3, 5 in this order */

    input = fopen("poly1.txt", "r" );
    if ((input = fopen("Poly1.txt","r")) == NULL)
      {
	printf("Could not open file: ");
	exit(0);
      }
    while(fscanf(input, "%d", &x) != EOF)
    {
      for(i=0; i<2; i++)
      {
	
	a[i] = x;
	x = a[i];
      }
      
      if(x == ' ' || x == '\n')
      {
      }
      else{
	intPtr = (int *) malloc(sizeof(int));
	*intPtr = x;
	printf("Inserting %d\n", *intPtr);
	insert_node (list, intPtr);
	temp2 = -1;
      }
      
    }
    

}
