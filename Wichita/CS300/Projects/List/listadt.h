#include "list_adt_impl.h"

LIST *createList (int (*compare_from_appl) (void *arg1, void *arg2));

void insert_node (LIST *list, void *ptr);;


void delete_node (LIST *list, void *ptr, void **dataOutPtr);

void destroyList(LIST *list);

void printList(LIST *list);

int addition(LIST *list, LIST *list2);

