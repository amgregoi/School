/************************************************************
 *Andy Gregoire                                             *
 *j455z944                                                  *
 *Summary: Reads in two files that each build an equation,  *
 *each line of the document contains the base and exponent  *
 *and builds the equations as (base)x^(exponent), afterwards*
 *it adds the two equations together                        *
 ************************************************************/


#include "List/listadt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int compare_appl (void *arg1, void *arg2)
{
    int *ptr1, *ptr2;
    ptr1 = (int *) arg1;
    ptr2 = (int *) arg2;

//    printf("\n comparing %d and %d, result = %d\n", *ptr1, *ptr2, (*ptr1 > *ptr2));
    if (*ptr1 > *ptr2)
	return 0; // True arg1 > arg2

    return 0;
}

int main()
{
    FILE *input;
    int x=0, count=0;
    test *ptr;

    LIST * list = createList (compare_appl);   /* Empty list for poly1 */

    

    printf("\n\nPoly1\n\n");
    if ((input = fopen("Poly1.txt","r")) == NULL){
        printf("Could not open file: ");
        exit(0);
    }
    else{
        while(fscanf(input, "%d", &x) != EOF){
            if(x == '\n' || x == ' '){
                continue;
            }
            else if(count == 0){
                ptr = (test *) malloc(sizeof(test));
                ptr->coef = x;
                count++;
            }
            else if(count == 1){
                ptr->power = x;
                count--;
                insert_node(list, ptr);
            }
        }
    }
    
    fclose(input);      //close poly1
    printList(list);

    LIST * list2 = createList (compare_appl);   /* empty list for poly2 */


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
            if(x == '\n' || x == ' '){
                continue;
            }
            else if(count == 0){
                ptr = (test *) malloc(sizeof(test));
                ptr->coef = x;
                count++;
            }
            else if(count == 1){
                ptr->power = x;
                count--;
                insert_node(list2, ptr);;
            }
        }
    }
    
    
    fclose(input);    //close poly2
    printList(list2);
    addition(list, list2);


    exit(0);

}
