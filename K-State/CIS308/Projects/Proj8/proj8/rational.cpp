#include "rational.h"
#include <iostream>

#define ABS(x) (x)<0?(-1)*(x):(x)

using namespace std;

Rational::Rational(int num, int denom) : Real(num/(double)denom) {
	this->num = num;
	this->denom = denom;
}
                
Rational::~Rational() {
	//delete stuff
}
                
double Rational::value() {
	return num/(double)denom;
}
                
Number* Rational::plus(Number *n) {
	if (dynamic_cast<Rational*>(n) != 0) {
		Rational *temp = (Rational *)n;
		int newNum = num*temp->denom + temp->num*denom;
		int newDenom = denom*temp->denom;
		return new Rational(newNum, newDenom);
        }
	return Real::plus(n);
}

Number* Rational::minus(Number *n) {
	if (dynamic_cast<Rational*>(n) != 0) {
		Rational *temp = (Rational *)n;
		int newNum = num*temp->denom - temp->num*denom;
		int newDenom = denom*temp->denom;
		return new Rational(newNum, newDenom);
        }
	return Real::minus(n);
}

Number* Rational::times(Number *n) {
	if (dynamic_cast<Rational*>(n) != 0) {
		Rational *temp = (Rational *)n;
		int newNum = num*temp->num;
		int newDenom = denom*temp->denom;
		return new Rational(newNum, newDenom);
        }
	return Real::times(n);
}

void Rational::print() {
	reduce();
	cout << num << "/" << denom << endl;
}

void Rational::reduce() {
	int i;
	int absNum = ABS(num);
	for (i = 2; i <= absNum; i++) {
		if (num%i == 0 && denom%i == 0) {
			num = num/i;
			denom = denom/i;
			i--;
		}
	}
}
