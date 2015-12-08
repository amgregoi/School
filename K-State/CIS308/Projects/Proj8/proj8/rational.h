#include "real.h"

#ifndef RATIONAL_H
#define RATIONAL_H

class Rational: public Real {
	protected:
		int num;
		int denom;
	public:
		/**
		 * Constructs the rational num/denom.
		 *
		 * num: the numerator
		 * denom: the denominator
		 */
		Rational(int num, int denom);

		/**
		 * Cleans up memory for this number
		 */
		~Rational();

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
	private:
		/**
		 * Reduces this fraction to lowest terms
		 */
		void reduce();
};

#endif
