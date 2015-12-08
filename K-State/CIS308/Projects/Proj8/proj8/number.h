#ifndef NUMBER_H
#define NUMBER_H

class Number {
	public:

		/**
		 * Computes the double value of this number
		 *
		 * return: the double value of this number
		 */
		virtual double value() = 0;

		/**
		 * Adds this number and the specified number
		 *
		 * n: the number to add to
		 * return: a number representing the result
		 *	of the addition
		 */
		virtual Number* plus(Number *n) = 0;

		/**
		 * Subtracts the specified number from this number
		 *
		 * n: the number to subtract
		 * return: a number representing the result
		 *	of the subtraction
		 */
		virtual Number* minus(Number *n) = 0;

		/**
		 * Multiplies this number and the specified number
		 *
		 * n: the number to multiply by
		 * return: a number representing the result
		 *	of the multiplication
		 */
		virtual Number* times(Number *n) = 0;

		/**
		 * Prints this number to the screen
		 */
		virtual void print() = 0;
};

#endif
