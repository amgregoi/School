#include "real.h"
#include "rational.h"
#include "integer.h"
#include <iostream>
#include <cstring>

using namespace std;

Number *num1, *num2;
char op;
char buffer[101];


double power(int base, int exp) {
	double result = 1;
	int i;
	for (i = 0; i < exp; i++) {
		result = result*base;
	}
	return result;
}

/**
 * toReal returns the real value
 * real.decimal
 *
 * real: the whole part of the number
 * decimal: the decimal part of the number
 *
 * returns: the corresponding decimal value
 */
double toReal(int real, int decimal) {
	int length = 0;
	int temp = decimal; 
	while (temp != 0) {
		length++;
		temp = temp/10;
	}
	return real + (decimal / power(10,length));
}

/**
 * parseInput reads the expression (stored in
 * buffer) and creates num1 and num2 to be
 * new numbers of the appropriate type and
 * value.  The operator of the expression
 * is stored in op.
 */
void parseInput() {
	int nums[4];
	int opPos;
	char tempBuff[101];
	strcpy(tempBuff, buffer);
	char *token = strtok(tempBuff, " /.+*-");
	
	int i = 0;
	while (token != 0) {
		nums[i++] = atoi(token);
		token = strtok(0, " /.+*-");
	}

	strcpy(tempBuff, buffer);
	token = strtok(tempBuff, "123456789./ ");
	op = *token;
	opPos = strcspn(buffer, &op);

	if (i == 2) {
		num1 = new Integer(nums[0]);
		num2 = new Integer(nums[1]);
	}
	if (strcspn(buffer, "/") < opPos) {
		if (i == 3) num2 = new Integer(nums[2]);
		num1 = new Rational(nums[0], nums[1]);
	}
	if (strcspn(buffer+opPos, "/") < strlen(buffer+opPos)) {		
		if (i == 3) {
			num1 = new Integer(nums[0]);
			num2 = new Rational(nums[1], nums[2]);
		}
		else num2 = new Rational(nums[2], nums[3]);
	}
	if (strcspn(buffer, ".") < opPos) {
		if (i == 3) num2 = new Integer(nums[2]);
		num1 = new Real(toReal(nums[0], nums[1]));
	}
	if (strcspn(buffer+opPos, ".") < strlen(buffer+opPos)) {
		if (i == 3) {
			num1 = new Integer(nums[0]);
			num2 = new Real(toReal(nums[1], nums[2]));
		}
		else num2 = new Real(toReal(nums[2], nums[3]));
	}
}

/**
 * main reads an arithmetic expression, parses
 * it into two numbers and an operation, and
 * calls the appropriate functions to evaluate
 * the expression.
 */
int main() {
	Number *result;
	cout << "Enter an arithmetic expression: ";
	cin.getline(buffer, 100);

	parseInput();

	switch (op) {
		case '+': 
			result = num1->plus(num2);
			break;
		case '-':
			result = num1->minus(num2);
			break;
		case '*':
			result = num1->times(num2);
			break;
		default:
			cout << "Invalid argument: " << op << endl;
			return 0;
	}
	cout << "Result : ";
	result->print();

	delete result;
	system("PAUSE");

	return 0;
}
