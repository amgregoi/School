#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
  int i;
  FILE *fp = fopen("somefile", "w");

  printf("\n argc = %d\n", argc);
  printf("\n argv[0] = %s\n", argv[0]);

  if (argc != 2)
  {
    printf("\n Usage:   ./a.out <argument> \n");
  }
  else
  {
    printf ("\n Argument you entered = %s\n", argv[1]);
    i = atoi(argv[1]);
    printf("\n i = %d\n", i);
  }

  fprintf (fp, "i = %d\n", i);
  fclose (fp);
  return 1;
}
