#include <stdio.h>
int number_of_steps = 0;
int n = 4;
void towers(int numdisks, char source, char dest, char aux)
{
    static int step = 0;
    /* Base Case */
    if (numdisks == 1)
    {
	printf("\nStep %d: Move ONE disk from %c to %c\n", ++step, source, dest);
	number_of_steps++;
	return;
    }

    /* General Case */
    towers(numdisks - 1, source, aux, dest);

    printf("\nStep %d: Move ONE disk from %c to %c\n", ++step, source, dest);
    number_of_steps++;
    
    towers(numdisks - 1, aux, dest, source);
    return;
}
int main()
{
   printf("\n N = %d\n", n);
   /* Source needle = A, Auxiliary needle = B, Destination needle = C */
   towers (n, 'A', 'C', 'B');

   printf("\n Total # of steps = %d\n", number_of_steps);
   return 0;
}

