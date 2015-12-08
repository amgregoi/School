#include "real.h"
#include <iostream>

using namespace std;

Real::Real(double val) {
	this->val = val;
}
                
Real::~Real() {
	//delete stuff
}
                
double Real::value() {
	return val;
}
                
Number* Real::plus(Number *n) {
	return new Real(val + ((Real *)n)->value());
}

Number* Real::minus(Number *n) {
	return new Real(val - ((Real *)n)->value());
}

Number* Real::times(Number *n) {
	return new Real(val * ((Real *)n)->value());
}

void Real::print() {
	cout << val << endl;
}

