#include <stdio.h>

#define I 100000
#define J 2500001


int gcd (int a, int b)
{
  /* Base Case */
  if (a == 0)
	return b;
  if (b == 0)
	return a;
  /* General Case */
  return gcd(b, a % b);
}

int main()
{
  printf("\n GCD of  %d, and %d = %d\n", I, J, gcd(I, J));
  return 0;
}


