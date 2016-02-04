#include <stdio.h>

int main()
{

int path[5][5] = {{0,2,5,6,50}, {2,0,3,7,4}, {5,3,0,4,8}, {6,7,4,0,5}, {50,4,8,5,0}};

int i, j, input, active=0, total=0;

for(j=0; j<24; j++){
	for(i=0; i<5; i++)
	{
		scanf("%d", &input);
		total+= path[active][input-1];
		active = input-1;

	}
	printf("Path %d(cost): %d\n", j, total);
	total=0;
	active=0;
}

}
