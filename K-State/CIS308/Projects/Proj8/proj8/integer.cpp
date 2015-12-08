#include "integer.h"
#include <iostream>

using namespace std;

Integer::Integer(int num) : Rational(num, 1) {
}
                
Integer::~Integer() {
	//delete stuff
}
                
double Integer::value() {
	return (double)num;
}
                
Number* Integer::plus(Number *n) {
	if (dynamic_cast<Integer*>(n) != 0) {
		Integer *temp = (Integer *)n;
		return new Integer(num+temp->num);
	}
	else if (dynamic_cast<Rational*>(n) != 0) {
        	return Rational::plus(n);
	}
	return Real::plus(n);
}

Number* Integer::minus(Number *n) {
	if (dynamic_cast<Integer*>(n) != 0) {
		Integer *temp = (Integer *)n;
		return new Integer(num-temp->num);
	}
	else if (dynamic_cast<Rational*>(n) != 0) {
        	return Rational::minus(n);
	}
	return Real::minus(n);
}

Number* Integer::times(Number *n) {
	if (dynamic_cast<Integer*>(n) != 0) {
		Integer *temp = (Integer *)n;
		return new Integer(num*temp->num);
	}
	else if (dynamic_cast<Rational*>(n) != 0) {
        	return Rational::times(n);
	}
	return Real::times(n);
}

void Integer::print() {
	cout << num << endl;
}
