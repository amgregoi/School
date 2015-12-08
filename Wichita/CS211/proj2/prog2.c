/***********************************
* Andy Gregoire                    *
*amgregoi                          *
*j455z944                          *
************************************/

# include <stdio.h> /* needed to perform input &  output */

int main()
{
  /* Declaration Section */
  int Coupons,
      Candybar,
      Gumball,
      Couponsremainder;
  
  printf( "enter the number of Coupons" ); /* asks number of coupons */
  scanf( "%d", &Coupons);
  
  while( Coupons >= 0 ) /* Keeps from allowing negative number of coupons */
  {     
     Candybar =  (Coupons / 10);
     Gumball = (Coupons%10 / 3);
     Couponsremainder = ((Coupons % 10) % 3);
     
  printf( "%d Candy Bars is %d Coupons(s)\n", Candybar, Coupons );
  printf( "%d Gumballs is   %d Coupon(s)\n", Gumball, Coupons ); 
  printf( "You have %d number of Coupons Remaining\n", Couponsremainder);
  scanf( "%d", &Coupons);
  }
  return 0;
}
     

  