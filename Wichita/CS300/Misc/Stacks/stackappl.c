#include <stackadt.h>

main()
{
    int *intPtr;
    STACK *stack = createStack ();

    /* Push 1, 2, 3 */
    intPtr = (int *) malloc(sizeof(int)); *intPtr = 1;
    printf("\n Pushing %d", *intPtr);
    push(stack, intPtr);
    intPtr = (int *) malloc(sizeof(int)); *intPtr = 2;
    printf("\n Pushing %d", *intPtr);
    push(stack, intPtr);
    intPtr = (int *) malloc(sizeof(int)); *intPtr = 3;
    printf("\n Pushing %d", *intPtr);
    push(stack, intPtr);

    printStack(stack);

    /* Pop integers */
    intPtr = (int *) popStack(stack);
    printf("\n Popped %d", *intPtr);
    free(intPtr);

    intPtr = (int *) popStack(stack);
    printf("\n Popped %d", *intPtr);
    free(intPtr);

    intPtr = (int *) popStack(stack);
    printf("\n Popped %d", *intPtr);
    free(intPtr);

    printStack(stack);
    printf("\n Stack is %s\n", emptyStack(stack) ? "Empty" : "Not Empty");

    destroyStack(stack);

}
