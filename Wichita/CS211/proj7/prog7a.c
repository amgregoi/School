/****************************************************
 *Andy Gregoire                                      *
 *j455z944                                           *
 *Sales Commission - How many salespeople earned     *
 *within a certain range                             *
 ****************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>


void randomx(int *b);


int main()
{
    int z, commission;
    int range[9] = {0,0,0,0,0,0,0,0,0};
    srand(time(NULL));
    
    for(z=0; z<50; z++)
    {
        randomx(&commission);
        
        
        if(commission < 300){
            range[0]++;
        }
        else if(commission < 400){
            range[1]++;
        }
        else if(commission < 500){
            range[2]++;
        }
        else if(commission < 600){
            range[3]++;
        }
        else if(commission < 700){
            range[4]++;
        }
        else if(commission < 800){
            range[5]++;
        }
        else if(commission < 900){
            range[6]++;
        }
        else if(commission < 1000){
            range[7]++;
        }
        else{
            range[8]++;
        }
        
    }
    
    printf("%d people in the 200-299 dollar range\n", range[0]);
    printf("%d people in the 300-399 dollar range\n", range[1]);
    printf("%d people in the 400-499 dollar range\n", range[2]);
    printf("%d people in the 500-599 dollar range\n", range[3]);
    printf("%d people in the 600-699 dollar range\n", range[4]);
    printf("%d people in the 700-799 dollar range\n", range[5]);
    printf("%d people in the 800-899 dollar range\n", range[6]);
    printf("%d people in the 900-999 dollar range\n", range[7]);
    printf("%d people in the 1000 or more dollar range\n", range[8]);
    
    exit(0);
}


void randomx(int *b){
    int a;
    a = rand()%1000;
    *b = 200 + a;
    
}







