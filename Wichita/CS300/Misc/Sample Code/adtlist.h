#include <stdio.h>
#include <stdlib.h>

typedef struct node {
         void *dataPtr;
  struct node *link;
} NODE;

NODE *createNode (void *itemPtr)
{
  NODE *nodePtr;
  nodePtr = (NODE *) malloc (sizeof(NODE));
  nodePtr->dataPtr = itemPtr;
  nodePtr->link = NULL;
  return nodePtr;
}

void *larger (void *dataPtr1, void *dataPtr2, int (*ptrToCmpFun) (void *, void *))
{
  if ((*ptrToCmpFun) (dataPtr1, dataPtr2) > 0)
    return dataPtr1;
  else
    return dataPtr2;
}

