#include <string.h>
#include <stdio.h>

void findAnagrams(char*, char*);

int main() {
	char word[100];
	char before[100];
	before[0] = '\0';
	printf("Enter a word: ");
	scanf("%s", word);
	
	findAnagrams(before, word);
	
	return 0;
}

void findAnagrams(char* first, char* second) {
	if (strlen(second) <= 1) {
		printf("%s%s\n", first, second);
	}
	else {
		int i, j;
		for (i = 0; i < strlen(second); i++) {
			char letter = second[i];
			char rest[100];
			char before[100];
			strcpy(rest, second);
			for (j = i; j < strlen(second); j++) {
				rest[j] = rest[j+1];
			}
			
			rest[strlen(second)-1] = '\0';
			strcpy(before, first);
			before[strlen(first)] = letter;
			before[strlen(first)+1] = '\0';
			
			findAnagrams(before, rest);
		}
	}
}