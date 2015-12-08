/****************************************************
 *Andy Gregoire                                      *
 *j455z944                                           *
 *Plays number guessing game                         *
 ****************************************************/

#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>

int userGuess(int guess, int number){
    int newGuess;
    
    if(guess > number) printf("Too high. Try again\n");
    else if(guess < number) printf("Too low. Try again\n");
    else return -1;
    
    printf("Please enter your next guess: ");
    scanf("%d", &newGuess);
    return userGuess(newGuess, number);
    
}

/* starts new game and asks for first guess */
int newGame(){
    int guess;
    
    printf("\nI have a number between 1 and 1000\n");
    printf("Can you guess my number?\n");
    printf("Please enter your guess: ");
    scanf("%d", &guess);
    return guess;
    /* picks random number */
}

bool continuePlaying(){
    char choice;
    
    printf("Excellent! you guesed the number!\n");
    while(true){
        printf("Would you like to play again (y or n)?: ");
        scanf("%s", &choice);
        //choice = getchar();
        
        if(choice == 'y') return true;
        if(choice == 'n') return false;
    }
}


int main(){
    
    bool playing = true;
    int number, guess;
    
    srand(time(NULL));
    number = (1 + (rand() % 4));
    
    while(playing){
        guess = newGame();
        if(userGuess(guess, number) == -1){
            number = (1 + (rand() % 4));    // new number if we decide to keep playing
            playing = continuePlaying();
        }
    }
    printf("Thank you for playing!\n");
}



