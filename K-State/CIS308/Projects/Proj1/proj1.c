#include <stdio.h>

int biggestPower2(int);

void printBinary(int, int);

int main() {
	int num, i;
	printf("Enter the number to count up to: ");
	scanf("%d", &num);
	
	for (i = 0; i <= num; i++) {
		int power = biggestPower2(i);
		printBinary(i, biggestPower2(i));
	}
	
	return 0;
}

int biggestPower2(int decimal) {
	if (decimal <= 1) return 1;
	else return 2*biggestPower2(decimal/2);
}

void printBinary(int decimal, int power2) {
	if (power2 == 1) {
		printf("%d\n", decimal);
	}
	else {
		int digit = decimal/power2;
		printf("%d", digit);
		if (digit == 1) {
			printBinary(decimal - power2, power2/2);
		}
		else {
			printBinary(decimal, power2/2);
		}
	}
}