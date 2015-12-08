/* List ADT: Not Assuming anything: could be a list of any data type */

#include <stdio.h>
#include <stdlib.h>

typedef struct A {
	void 		*dataPtr;
	struct A*	link;
} NODE;

typedef struct B {
	int 		count;
	NODE*		head;
	NODE*		rear;
	NODE*		pos;
	int 		(*compare) (void *arg1, void *arg2);
} LIST;

typedef struct poly
{
  int power;
  int coef;
}test;

// Creates an empty list
LIST *createList (int (*compare_from_appl) (void *arg1, void *arg2))
{
    LIST* list;

    list = (LIST *) malloc (sizeof(LIST));
    if (!list) {
        printf("No memory available, Sorry !\n");
        return list;
    }

    list->count = 0;
    list->head = list->pos = list->rear = NULL;
    list->compare = compare_from_appl;

    return list;
}

//internal function. Needs to set pPre and pLoc pointers in the list
// return whether element (ptr) found or not
int search (LIST *list, NODE** pPre, NODE** pLoc, void *ptr)
{
    int found;
    *pPre = *pLoc = NULL;
    *pLoc = list->head;

    // traverse list 
    while ((*pLoc != NULL) &&  (((* list->compare)  ((*pLoc)->dataPtr, ptr)) == 0 )){
        *pPre = *pLoc;
        *pLoc = (*pLoc)->link;
    }
    
    // pPre and pLoc are correctly set
    if ((*pLoc) == NULL)
        found = 0;
    else if ((( (* list->compare)  ((*pLoc)->dataPtr, ptr) ) > 0 ))
        found = 0;
    else if  (((* list->compare)  ((*pLoc)->dataPtr, ptr) ) == 0 )
        found = 1;

    return found;
}



// Internal (private) function
void insert (LIST *list, NODE *pPre, void *ptr)
{
    NODE *pNew = (NODE *) malloc (sizeof(NODE));

    pNew->dataPtr = ptr;
    pNew->link = NULL;

    // Inserting at the beginning of the list, or inserting in empty list
    if (pPre == NULL){
        pNew->link = list->head;
        list->head = pNew;
    }
    else{ // inserting in the middle or end
        pNew->link = pPre->link;
        pPre->link = pNew;
    }

    if (pNew->link == NULL) // we inserted in empty list
        list->rear = pNew;
    
    list->count++;
    return;
}


// Public Function
void insert_node (LIST *list, void *ptr)
{
    NODE *pPre, *pLoc;
    int found;

    found = search (list, &pPre, &pLoc, ptr);

    // Non duplicate list
    if (found == 1)
        return;

    insert (list, pPre, ptr);
    return;
}


void printList(LIST *list)
{
    NODE *temp = list->head;
    int count = 1;
    test *temp1;

    if (!temp) { printf ("\n Empty List \n"); return; }

    while (temp){
        temp1 = temp->dataPtr;
        printf("\n Element  %d = %dx^%d \n", count, temp1->coef, temp1->power);
        count++;
        temp = temp->link;
    }
    return;
}

int addition(LIST *list, LIST *list2)
{
    int x,y;
    test *temp1;
    test *temp2;
    NODE *ptr1=list->head;
    NODE *ptr2=list2->head;
    printf("\n\n");
    
    while(ptr1 != NULL && ptr2 != NULL)
    {

        temp1=(test *)ptr1->dataPtr;
        temp2=(test *)ptr2->dataPtr;

        if(temp1->power == 0){
            x = temp1->coef;
            printf("0 %d", x);
            return 0;
        }
        
        if(temp2->power == 0){
            x = temp2->coef;
            printf("0 %d", x);
            return 0;
        }
        
        if(temp1->power == temp2->power){
            x = temp1->coef+temp2->coef;
            y = temp1->power;
            ptr1=ptr1->link;
            ptr2=ptr2->link;
            printf("%dx^%d +", x, y);
        }

        if(temp1->power < temp2->power){
            x = temp2->coef;
            y = temp2->power;
            ptr2 = ptr2->link;
            printf("%dx^%d +", x, y);
        }

        if(temp1->power > temp2->power){
            x = temp1->coef;
            y = temp1->power;
            ptr1=ptr1->link;
            printf("%dx^%d + ", x,y);
        }
    }
    printf("\n");
    exit (0);
}


