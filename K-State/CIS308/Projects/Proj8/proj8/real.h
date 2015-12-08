#include "number.h"

#ifndef REAL_H
#define REAL_H

class Real: public Number {
	private:
		double val;
	public:
		/**
		 * Constructs a new real number
		 *
		 * val: the value of the real number
		 */
		Real(double val);

		/**
		 * Cleans up memory for this number
		 */
		~Real();

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
		 * return: a real number representing the result
		 *	of the addition
		 */
		Number* plus(Number *n);

		/**
		 * Subtracts the specified number from this number
		 *
		 * n: the number to subtract
		 * return: a real number representing the result
		 *	of the subtraction
		 */
		Number* minus(Number *n);

		/**
		 * Multiplies this number and the specified number
		 *
		 * n: the number to multiply by
		 * return: a real number representing the result
		 *	of the multiplication
		 */
		Number* times(Number *n);

		/**
		 * Prints this number to the screen
		 */
		void print();
};

#endif
