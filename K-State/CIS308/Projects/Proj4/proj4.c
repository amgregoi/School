#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {false = 0, true} BOOL;

typedef struct trie {
	char letter;
	BOOL isWord;
	struct trie* children[26];
} TRIE;

TRIE* root;
char* alpha = "abcdefghijklmnopqrstuvwxyz";

int indexOf(char letter) {
	int i;
	for (i = 0; i < strlen(alpha); i++) {
		if (letter == alpha[i]) return i;
	}
	
	return -1;
}

TRIE* getChild(TRIE* node, char letter) {
	return node->children[indexOf(letter)];
}

void addChild(TRIE* parent, TRIE* child) {
	parent->children[indexOf(child->letter)] = child;
}

void add(char* word) {
	TRIE* curTrie = root;
	TRIE* temp;
	int i, j;
	
	for (i = 0; i < strlen(word); i++) {
		char curChar = word[i];
		temp = getChild(curTrie, curChar);
		
		//path does not exist -- need to add a new node
		if (temp == NULL) {
			temp = malloc(sizeof(TRIE));
			temp->letter = curChar;
			temp->isWord = false;
			for (j = 0; j < strlen(alpha); j++) {
				temp->children[j] = NULL;
			}
			addChild(curTrie, temp);
		}
		curTrie = temp;
	}
	
	//curTrie represents the word we added
	curTrie->isWord = true;	
}

BOOL search(char* word) {
	TRIE* curTrie = root;
	int i;
	
	for (i = 0; i < strlen(word); i++) {
		char curChar = word[i];
		curTrie = getChild(curTrie, curChar);
		if (curTrie == NULL) {
			return false;
		}
	}
	
	return (i == strlen(word) && curTrie->isWord);
}

void buildTrie(char* filename) {
	FILE* fp = fopen(filename, "r");
	char buff[30];
	if (fp != NULL) {
		while (fscanf(fp, "%s", buff) != EOF) {
			add(buff);
		}
	}
	
	fclose(fp);
}

void printAnagrams(char* first, char* second) {
	if (strlen(second) < 1 && search(first) == true) {
		printf("%s\n", first);
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
			
			printAnagrams(before, rest);
		}
	}
}

void releaseTrie(TRIE* top) {
	int i;
	if (top == NULL) return;
	for (i = 0; i < strlen(alpha); i++) {
		if (top->children[i] != NULL) releaseTrie(top->children[i]);
	}
	
	free(top);
}

int main(int argc, char* argv[]) {
	if (argc != 2) {
		printf("Please supply dictionary filename as command-line argument.");
	}
	else {
		char word[100];
		char before[100];
		int i;
		root = malloc(sizeof(TRIE));
		root->letter = '\0';
		root->isWord = false;
		for (i = 0; i < strlen(alpha); i++) {
			root->children[i] = NULL;
		}
		
		buildTrie(argv[1]);
		before[0] = '\0';
		printf("Enter a word: ");
		scanf("%s", word);
		
		printAnagrams(before, word);
		
		releaseTrie(root);
	}
	
	return 0;
}