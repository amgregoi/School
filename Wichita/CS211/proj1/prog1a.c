/************************************************************
 *Andy Gregoire                                             *
 *j455z944                                                  *
 *Summary: Reads in a user input string and prints out the  *
 *length of that string                                     *
 ************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
  char str[80];
  int i;

  fgets(str, 80, stdin);


  i = strlen(str) - 1;
  if( str[ i ] == '\n')
      str[i] = '\0';

  printf("%d\n", i);

  return 0;
}
