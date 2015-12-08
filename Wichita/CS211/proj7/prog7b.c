#include <stdio.h>

#include <stdlib.h> 
 #define TRUE 1
 #define FALSE 0
 #define SIZE 8
 #define SIXE 1


void SetBoard (int **board, int x, int col);
void DisplayBoard (int **board, int row, int col);
int Tour (int **board, int xP, int yP, int row, int col,
int moveNum);


int main()
{
 int row, col, xP, yP;
 int **board;
 int a, i;
 
 row = SIZE;
 col = SIZE;
 xP = SIXE;
 yP = SIXE;
 
 printf("Rows: %u; Columns: %u\n", row, col);
 printf("Starting position: X: %u; Y: %u\n", xP, yP);
 printf("Initializing Board\n");
 
    // Convert to zero-based coordinates.
    xP--;
    yP--;
 

 
    board = calloc(row, sizeof(int *));
    int **temp = board;
 
    for (i = 0; i < row; i++)
     {	
      board[i] = calloc(col, sizeof(int));

     }
 
   SetBoard (board, row, col);
   DisplayBoard (board, row, col);
 
   printf("Finding...\n");
    if (Tour (board, xP, yP, row, col, 1))
    {
      printf("Solution:\n\n");
    }
      else
      {
	printf("No solution.\n\n");
      }
  DisplayBoard (board, row, col);
 
  temp = board;
  for (i = 0; i < row; i++)
  {
    free(*temp);
    (temp)++;
  }
 

 
 return 0;
 }
 
 void SetBoard (int **board, int row, int col)
 {
 int x, y;
 
 for (x = 0; x < row; x++)
 {
  for (y = 0; y < col; y++)
   {
    board[x][y] = 0;
    }
  }
 }
 
 void DisplayBoard (int **board, int row, int col)
 {
 int x, y;
 
   for (x = 0; x < row; x++)
    {
      for (y = 0; y < col; y++)
      {
	printf("%4d", board[x][y]);
      }
	printf("\n");
    }
  }
 
 int CheckMove (int **board, int xP, int yP, int row, int col, int moveNum)
  {
    if ((xP < 0) || (xP >= row))
  {
 return FALSE;
  }	
 
 if ((yP < 0) || (yP >= col))
 {
 return FALSE;
 }
 
 if (board[xP][yP] && board[xP][yP] < moveNum)
  {
  return FALSE;
  }
 
 return TRUE;
 }
 
 int Tour (int **board, int xP, int yP, int row, int col,
 int moveNum)
 {
 if (!CheckMove (board, xP, yP, row, col, moveNum))
 {
 return FALSE;
 }
 
 board[xP][yP] = moveNum;
 
 if ((row * col) == moveNum)
 {
 return TRUE;
 }
 

 
 if (!Tour
  (board, (xP + 1), (yP + 2), row, col, (moveNum + 1)))
    if (!Tour
      (board, (xP - 2), (yP + 1), row, col, (moveNum + 1)))
	if (!Tour
	  (board, (xP - 2), (yP - 1), row, col, (moveNum + 1)))
	    if (!Tour
	      (board, (xP - 1), (yP + 2), row, col, (moveNum + 1)))
		if (!Tour
		  (board, (xP - 1), (yP - 2), row, col, (moveNum + 1)))
		    if (!Tour
		      (board, (xP + 2), (yP + 1), row, col,
		      (moveNum + 1)))
			if (!Tour
			  (board, (xP + 2), (yP - 1), row, col,
			  (moveNum + 1)))
			     if (!Tour
			      (board, (xP + 1), (yP - 2), row, col,
			      (moveNum + 1))) {
			      board[xP][yP] = row * col;
 return FALSE;
 }

 moveNum = 0;
 return TRUE;
}