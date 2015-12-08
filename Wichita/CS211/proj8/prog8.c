/****************************************************
 *Andy Gregoire                                      *
 *j455z944                                           *
 *Text document analyzer                             *
 ****************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#define FILE_TITLE "gettysburg.txt"

int mainMenu();
void control();
void countLines();
void countWords();
void countCharacters();
void countSentences();


int main(){
    control();
}

/* controls what to do after the user makes a choice */
void control(){
    
    int choice = mainMenu();
    system("@cls||clear");
    
    switch (choice) {
        case 1:
            countLines();
            break;
        case 2:
            countWords();
            break;
        case 3:
            countCharacters();
            break;
        case 4:
            countSentences();
            break;
        case 5:
            countLines();
            countWords();
            countCharacters();
            countSentences();
            break;
        case -1:
            printf("Program exited\n");
            exit(0);
            break;
        default:
            printf("Oops try again\n");
            break;
    }
    control();
}

/* prints menu to terminal, and takes users input as choice */
int mainMenu(){
    int choice;
    printf("_______Menu_______\n");
    printf("1  - count lines\n");
    printf("2  - count words\n");
    printf("3  - count Characters\n");
    printf("4  - count sentences\n");
    printf("5  - count all\n");
    printf("-1 - quit\n");
    printf("What would you like to do?: ");
    scanf("%d", &choice);
    return choice;
}

/* Counts number of lines in a file */
void countLines(){
    FILE *file;
    int lineCount = 0;
    char buf[1000];
    
    if((file = fopen(FILE_TITLE, "r")) == NULL){
        printf("Couldn't open file\n");
        exit(0);
    }
    
    while(fgets(buf, sizeof(buf), file) != NULL){
        lineCount++;
    }
    
    printf("This file contains %d lines\n", lineCount);
    fclose(file);
}


/* Counts number of words in a file */
void countWords(){
    int charTest, wordLength, wordCount = 0;
    FILE *file;
    
    if((file = fopen(FILE_TITLE, "r")) == NULL){
        printf("Couldn't open file\n");
        exit(0);
    }
    
    while((charTest = fgetc(file)) != EOF){
        if(isalpha(charTest)){
            wordLength++;
        }
        else{
            wordLength = 0;
            wordCount++;
        }
    }
    
    printf("This file contains %d words\n", wordCount);
    fclose(file);
}

/* Counts number of characters in a file */
void countCharacters(){
    int characterCount = 0;
    
    FILE *file;
    if((file = fopen(FILE_TITLE, "r")) == NULL){
        printf("Could not open file\n");
        exit(0);
    }
    
    while((fgetc(file)) != EOF){
        characterCount++;
    }
    printf("This file contains %d characters (including spaces)\n", characterCount);
    fclose(file);
}

/* Counts number of sentences in a file */
void countSentences(){
    int sentenceCount = 0;
    int p;
    FILE *file;
    
    if ((file = fopen(FILE_TITLE, "r")) == NULL){
        printf("Could not open file: ");
        exit(0);
    }
    
    while((p = fgetc(file)) != EOF){
        if(p == '.' || p == '!' || p == '?')
            sentenceCount++;
    }
    printf("This file contains %d sentences\n", sentenceCount);
    fclose(file);
}




