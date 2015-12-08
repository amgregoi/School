#include <stdio.h>

#define MAX 45

int FIB [100];

int fib (int i)
{
  int result;
  /* Base case */
  if ((i == 0) || (i == 1)) 
	return i;

  if (FIB[i] != 0)
	return FIB[i];

  /* General Case */
  result = (fib(i - 1) + fib(i - 2));

  /* Here i is always > 1 */
  if (FIB[i] == 0)
	FIB[i] = result;

  return result;
}

int main()
{
  int i;
  for (i = 0; i < 100; i++)
	FIB[i] = 0;

  for (i = 0; i <= MAX; i++)
  {
    printf ("\n Fib Number %d = %d\n", i, fib(i));
  }
  return 0;
}
