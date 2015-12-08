#include "stackadt_impl.h"

STACK *createStack();

void push(STACK *stack, void *ptr);

void *popStack(STACK *stack);

STACK *destroyStack(STACK * stack);

void printStack(STACK *stack);

