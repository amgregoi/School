#include <stdio.h>
#define N 20


double fact(int j)
{
  double result;
  
  if (j == 0)
    result = 1;
  else
    result = j*fact(j-1);

  return result; 
}


int main ()
{
  double result;

  result = fact(N);
  printf("Factorial of %d is %lf\n", N, result);
  return 0;
}

