#include <stdio.h>

#define MAX 50

int fib (int i)
{
  int j, result, last, secondlast;

  /* Base Case */
  if ((i == 0) || (i == 1)) return i;

  last = 1;
  secondlast = 0;

  for (j = 2; j <= i; j++)
  {
	result = last + secondlast;
	secondlast = last;
	last = result;
  }
  return result;
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
