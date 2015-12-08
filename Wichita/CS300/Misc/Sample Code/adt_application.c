#include <adtlist.h>

int compare (void *ptr1, void *ptr2)
{
  if (*(char *) ptr1 >= *(char *) ptr2)
    return 1;
  else
    return -1;
}

int main()
{
  char *data1, *data2, *temp;
  void *largerInt;
  NODE *node;

  data1 = (char *) malloc (sizeof(char));
  *data1 = 'A';

  node = createNode(data1);
  temp = (char *) node->dataPtr;
  printf ("\n Data from node 1 = %c\n", *temp);

  data2 = (char *) malloc (sizeof(char));
  *data2 = 'B';

  node->link = createNode(data2);
  temp = (char *) node->link->dataPtr;
  printf ("\n Data from node 2 = %c\n", *temp);

  largerInt = larger (node->dataPtr, node->link->dataPtr, compare);
  temp = (char *) largerInt;
  printf ("\n Larger character = %c\n", *temp);

  return 0;
}
