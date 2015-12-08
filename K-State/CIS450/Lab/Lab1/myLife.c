/*
Andy Gregoire | David Parker
Lab 2 : Bit of Life
we were not able to get this to work on a 128x128 array but rather a 128x127
	It had a problem with the height & width being the same?

*/
#include <stdio.h>
#include <stdlib.h>

#define width 128
#define height 127



void randomizeworld(int *world[]){	
	for(int i = 0; i < height; i++){
		for(int j = 0; j< width; j++){
			int x = rand();
			if(x%2== 1)
				world[i][j] = 1;
			else
				world[i][j] = 0;
			//printf("%c ", world[i][j]);
		}	
		//printf("\n");
	}
		
	
}

void printworld(int *world[], FILE *pOutput){
	for(int i = 0; i < height; i++)
		for(int j = 0; j< width; j++){
			//printf("%d", world[i][j]);
			if((world[i][j]&1) == 1){
				fprintf(pOutput, "%c", 254);
				//printf("%c", 254);
				}
			else{
				fprintf(pOutput, " ");
				//printf(" ");
				}
				
		}
		printf("\n");
}

int isLessEqual(int x, int y) {
  int temp = x ^ y;
  int ret = ((~temp) & (y + ~x + 1)) | (y & temp);
  return !(ret >> 31 );
}

int isEqual(int x, int y){
	return !(x-y);
}

void update(int *world[]){
int neighbor = 0;
	for(int i = 0; i < height; i++){
		for( int j = 0; j< width; j++){
			neighbor = 0;
			if(j>0 && (world[i][j-1] == 1))	neighbor++;
			if( j<width && (world[i][j+1] == 1)) neighbor++;
			if(i>0 && (world[i-1][j] == 1)) neighbor++;
			if(i<height && (world[i+1][j] == 1)) neighbor++;
			if(j>0 && i>0 && (world[i-1][j-1] == 1)) neighbor++;
			if(j>0 && i<height && (world[i+1][j-1] == 1)) neighbor++;
			if(j<width && i>0 && (world[i-1][j+1] == 1)) neighbor++;
			if(j<width && i<height && (world[i+1][j+1] == 1)) neighbor++;	
			
			if(isLessEqual(neighbor, 1) || !isLessEqual(neighbor, 3))
				world[i][j] = 0;
			if(isEqual(world[i][j], 1) 	&& (isEqual(neighbor, 2) || isEqual(neighbor, 3)))
				world[i][j] = 1;
			if(isEqual(world[i][j], 0) && isEqual(neighbor, 3))
				world[i][j] = 1;
			//printf("%d : %d - %d,  %d\n",i, j, world[i][j], neighbor);
		}
	}		
}




int main(int arg, char *argv[])
{	
	int **world = (int **) malloc(width*sizeof(int));
	for(int i =0; i < width; i++)
		world[i] = (int *) malloc(height*(sizeof(int)));
		
	randomizeworld(*&world);
	
	do{
		printworld(*&world, stdout);
		getchar();
		fflush(stdin);
		update(*&world);
	}while(1);
	
	free(world);
	for(int i = 0; i< width; i++)
		free(world[i]);
		
}