/*
Andy Gregoire
Mike McCall
*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

void printArray(int* arr, int start, int end)
{
	int i;
	printf("----------------------\n");
	for(i=1;i<=end-start+1; i++)
                printf("%d\n", arr[i]);
	printf("----------------------\n");
}

void swap(int *x, int *y)
{
	int temp = *x;
	*x = *y;
	*y = temp;
}

void slowsort(int* arr, int start, int end)
{
        int n = end - start;
        if(n == 1)
	{
                if(arr[start] > arr[end]){
                        swap(&arr[start], &arr[end]);
		}
        }
	else if(n > 1)
        {
                slowsort(arr, start, start+(int)ceil((2*(n+1))/3.0)-1);
		slowsort(arr, end-(int)floor(((2*n)/3.0)), end);
		slowsort(arr, start, start+(int)ceil((2*(n+1))/3.0)-1);

	}
}


int main()
{
	clock_t t1, t2;
        srand(time(NULL));
        int i,j,k, *arr = malloc(sizeof(int)), arr_length;
	float time;
	for(k=10; k<=500; k+=10){//arraylength
		arr_length = k;
		time = 0;
		for(j=0; j<500; j++){//number of times
        		for(i=1; i<=arr_length; i++)
			{
        		        arr[i] = rand()%1000;
			}
			t1 = clock()/(CLOCKS_PER_SEC/1000);
        		slowsort(arr, 1, arr_length);
			t2 = clock()/(CLOCKS_PER_SEC/1000);
			time+= ((float)t2 - (float)t1);
		}
		printf("%d, %.04f\n",k, time);
	}
	//printArray(arr,1, arr_length);
	exit(0);
}
