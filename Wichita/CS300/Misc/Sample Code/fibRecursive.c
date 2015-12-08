#include <stdio.h>

#define MAX 45

int fib (int i)
{
  /* Base case */
  if ((i == 0) || (i == 1)) 
	return i;

  /* General Case */
  return (fib(i - 1) + fib(i - 2));
}


int main()
{
  int i;

  for (i = 0; i <= MAX; i++)
  {
    printf ("\n Fib Number %d = %d\n", i, fib(i));
  }
  return 0;
}
