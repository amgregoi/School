#include <stdio.h>

typedef struct A {
    void 	*dataPtr;
    struct A	*link;
} NODE;

typedef struct B {
    int 	count;
    NODE	*top;
} STACK;

STACK * createStack ()
{
    STACK *stack = (STACK *) malloc(sizeof(STACK));
    if (!stack) {
	printf("\n Error No Memory available \n");
	return NULL;
    }
    stack->count = 0;
    stack->top = NULL;
    return stack;
}

void printStack (STACK *stack)
{
    int count = 1;
    NODE *tmp = stack->top;
    printf("\n");
    printf("\n Printing Stack Contents \n");
    if (!tmp) printf("\n Empty Stack");
    while (tmp)
    {
	printf("\n Element %d = %d ", count, *(int *)tmp->dataPtr);
	tmp = tmp->link;
	count++;
    }
    printf("\n");
    return;
}

void push(STACK *stack, void *ptr)
{
    NODE *temp = (NODE *) malloc (sizeof(NODE *));
    if (!temp) { printf ("\nError No Memory Available\n"); return; }
    
    temp->dataPtr = ptr;
    temp->link = stack->top;
    stack->top = temp;
    stack->count++;
    return;
}

void *popStack(STACK *stack)
{
    void *p;
    NODE *temp;
    if (stack->count == 0) return NULL;
    p = stack->top->dataPtr;
    temp = stack->top;
    stack->top = stack->top->link;
    free(temp);
    stack->count--;
    return p;
}

STACK * destroyStack (STACK * stack)
{
    while (stack->count > 0)
    {
	popStack(stack);
    }
    free(stack);
    return NULL;
}

int emptyStack (STACK * stack)
{
    if (stack->count == 0)
	return 1;
    else
	return 0;
}

/* Other functions : FullStack, StackCount, StackTop */

