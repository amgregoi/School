#include <stdio.h>

typedef struct {
  char c1;
  int i1;
  char c2;
  short s1;
  char c3;
}  A;

A a1;

int x;

void func1(A *ap, int i) {
  int m, n;

m = (ap->i1 * 4) + i; //lines 10,11,12,13

n = (ap->s1 * 2) + 3; //lines 14,15,16,17

x = m + n; //lines 17, 18, 19

ap->c1--; //line 20 - places ap->c1 into eax, 21 decrements c1

if(ap->c1 > 0) //lines 25 & 26 testing if we should go into recursive steps
{
	i++; // line 27, 28, 29
	func1(ap, i); //line 30 - updates i, 31 & 32 push parameters, 33 calls func 1
}

  // the body has been deleted
}

void main(int argc, char **argv, char **envp) {
  A *ap = &a1;


ap->c1 = 1;		//line 46
ap->i1 = ap->c1 + 2;	//line 47,48,49
ap->c2 = ap->i1 + 3;	//line 50, 51
ap->s1 = ap->c2 + 4;	//line 52, 53, 54,55,56
ap->c3 = ap->s1 + 5;	//line 57,58,59,60,61
func1(ap, ap->c3);	//62 - places ap->c3 into register, 63 & 64 push parameters for func1, 65 call func1

  // the first several lines of the body have been deleted

  printf("a1 = %d,\t%d,\t%d,\t%d,\t%d\n", a1.c1, a1.i1, a1.c2, a1.s1, a1.c3);
  printf("x = %d\n", x);
}
