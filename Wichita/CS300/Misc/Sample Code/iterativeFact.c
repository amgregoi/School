#include <stdio.h>
#define N 20

int main()
{
  double result = 1, i;
  
  for (i = 1; i <= N; i++)
  {
    result = result*i;
  }
  printf("Factorial of %d is %lf\n", N, result);
  return 0;
}



