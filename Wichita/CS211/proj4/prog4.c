/****************************************************
 *Andy Gregoire                                      *
 *j455z944                                           *
 *Draws an ascii box with the given size             *
 ****************************************************/

#include <stdio.h>

/* make sure user enters a number */
int userInput(){
    int size -2;
    
    while(size == -2){
        printf("Enter the size of the box (-1 to end): ");
        while(getchar() != '\n');   // clears input buffer, so program doesn't go crazy randomly
        scanf("%d", &size);
    }
}

int main(){
    
    int tempLength,
    i,j,
    size;
    
    size = userInput();
    
    while(size > 0 && size < 64){
        tempLength = (size * 3) - 1;
        
        /* top of the box */
        for(i = 0; i < tempLength; i++){
            printf("*");
        }
        printf("\n");
        
        /* mid section of the box */
        for(i = 0; i <= size; i++){
            for(j = 0; j <= size; j++){
                if(j == size || j == 0) printf("*");
                else printf("   ");
            }
            printf("\n");
        }
        
        /* bottom of the box */
        for(i = 0; i < tempLength; i++){
            printf("*");
        }
        printf("\n");
        
        /* make sure user enters a number */
        size = userInput();
    }
    
    return 0;
}

