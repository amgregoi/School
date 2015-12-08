#include "rational.h"

#ifndef INTEGER_H
#define INTEGER_H

class Integer: public Rational {
	public:
		/**
		 * Constructs the integer num.
		 *
		 * num: the integer
		 */
		Integer(int num);

		/**
		 * Cleans up memory for this number
		 */
		~Integer();

		/**
		 * Computes the double value of this number
		 *
		 * return: the double value of this number
		 */
		double value();

		/**
		 * Adds this number and the specified number
		 *
		 * n: the number to add to
		 * return: the most specific number representing 
		 *	the result of the addition
		 */
		Number* plus(Number *n);

		/**
		 * Subtracts the specified number from this number
		 *
		 * n: the number to subtract
		 * Adds this number and the specified number
		 *
		 * n: the number to add to
		 * return: the most specific number representing 
		 *	the result of the subtraction
		 */
		Number* minus(Number *n);

		/**
		 * Multiplies this number and the specified number
		 *
		 * n: the number to multiply by
		 * return: the most specific number representing 
		 *	the result of the multiplication
		 */
		Number* times(Number *n);

		/**
		 * Prints this number to the screen
		 */
		void print();
};

#endif
