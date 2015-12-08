/*************************************************
*Andy Gregoire					 *
*j455z944					 *
*Sales Commission - How many salespeople earned  *
*within a certain range 			 *				 
*ETA - 1.5 hour               			 *	 
*Acutal time - ~4 hours   			 *
**************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>


void randomx(int *b);


int main()
{
  int z,
      array[50],
      b;
  int d=0, e=0, f=0, g=0, h=0, i=0, j=0, k=0, l=0;
 
  srand(time(NULL));

  for(z=0; z<50; z++)
  {
    randomx(&b);
    array[z] = b;
    

  if(b >=200 && b <= 299)
  {
    d++;
  } 
  if(b >=300 && b <= 399)
  {
    e++;
  } 
  if(b >=400 && b <= 499)
  {
    f++;
  } 
  if(b >=500 && b <= 599)
  {
    g++;
  } 
  if(b >=600 && b <= 699)
  {
    h++;
  } 
  if(b >=700 && b <= 799)
  {
    i++;
  } 
  if(b >=800 && b <= 899)
  {
    j++;
  } 
  if(b >=900 && b <= 999)
  {
    k++;
  } 
  if(b >=1000)
  {
    l++;
  } 

  }
  
      printf("%d people in the 200-299 dollar range\n", d);
      printf("%d people in the 300-399 dollar range\n", e);
      printf("%d people in the 400-499 dollar range\n", f);
      printf("%d people in the 500-599 dollar range\n", g);
      printf("%d people in the 600-699 dollar range\n", h);
      printf("%d people in the 700-799 dollar range\n", i);
      printf("%d people in the 800-899 dollar range\n", j);
      printf("%d people in the 900-999 dollar range\n", k);
      printf("%d people in the 1000 or more dollar range\n", l);
  
  

  exit(0);
}
  

void randomx(int *b)
{ 
  int a;

    a = rand()%1000;
    
    *b = 200 + a;
  
}



    