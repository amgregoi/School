#include <stdio.h>

#include <stdlib.h> 
 #define TRUE 1
 #define FALSE 0


void InitializeBoard (int **board, int xSize, int ySize);
void DisplayBoard (int **board, int xSize, int ySize);
int KnightsTour (int **board, int xCoor, int yCoor, int xSize, int ySize,
int moveNum);
int main(int argc, char *argv[])
{
 int xSize, ySize, xCoor, yCoor;
 int **board;
 int a, i;
 
 xSize = ySize = 5;
 xCoor = yCoor = 3;
 
 printf("X: %u; Y: %u\n", xSize, ySize);
 printf("X Coor: %u; Y Coor: %u\n", xCoor, yCoor);
 
 // Convert to zero-based coordinates (as opposed to one-based).
 xCoor--;
 yCoor--;
 

 
 board = calloc(xSize, sizeof(int *));
 int **temp = board;
 
 for (i = 0; i < xSize; i++)
 {
  board[i] = calloc(ySize, sizeof(int));

 }
 
 InitializeBoard (board, xSize, ySize);
 DisplayBoard (board, xSize, ySize);
 

 printf("Executing Knight's Tour...\n");
 
 if (KnightsTour (board, xCoor, yCoor, xSize, ySize, 1))
 {
  printf("Solution found:\n\n");
 }
 else
 {
 printf("No solution found.\n\n");
 }
 DisplayBoard (board, xSize, ySize);
 
 temp = board;
 for (i = 0; i < xSize; i++)
 {
 free(*temp);
 (temp)++;
 }
 
 free(board);
 
 return 0;
 }
 
 void InitializeBoard (int **board, int xSize, int ySize)
 {
 int x, y;
 
 for (x = 0; x < xSize; x++)
 {
  for (y = 0; y < ySize; y++)
   {
    board[x][y] = 0;
    }
  }
 }
 
 void DisplayBoard (int **board, int xSize, int ySize)
 {
 int x, y;
 
   for (x = 0; x < xSize; x++)
    {
      for (y = 0; y < ySize; y++)
      {
	printf("%4d", board[x][y]);
      }
	printf("\n");
    }
  }
 
 int MoveIsValid (int **board, int xCoor, int yCoor, int xSize, int ySize, int moveNum)
  {
    if ((xCoor < 0) || (xCoor >= xSize))
  {
 return FALSE;
  }	
 
 if ((yCoor < 0) || (yCoor >= ySize))
 {
 return FALSE;
 }
 
 if (board[xCoor][yCoor] && board[xCoor][yCoor] < moveNum)
  {
  return FALSE;
  }
 
 return TRUE;
 }
 
 int KnightsTour (int **board, int xCoor, int yCoor, int xSize, int ySize,
 int moveNum)
 {
 if (!MoveIsValid (board, xCoor, yCoor, xSize, ySize, moveNum))
 {
 return FALSE;
 }
 
 board[xCoor][yCoor] = moveNum;
 
 if ((xSize * ySize) == moveNum)
 {
 return TRUE;
 }
 

 
 if (!KnightsTour
  (board, (xCoor + 1), (yCoor + 2), xSize, ySize, (moveNum + 1)))
    if (!KnightsTour
      (board, (xCoor - 2), (yCoor + 1), xSize, ySize, (moveNum + 1)))
	if (!KnightsTour
	  (board, (xCoor - 2), (yCoor - 1), xSize, ySize, (moveNum + 1)))
	    if (!KnightsTour
	      (board, (xCoor - 1), (yCoor + 2), xSize, ySize, (moveNum + 1)))
		if (!KnightsTour
		  (board, (xCoor - 1), (yCoor - 2), xSize, ySize, (moveNum + 1)))
		    if (!KnightsTour
		      (board, (xCoor + 2), (yCoor + 1), xSize, ySize,
		      (moveNum + 1)))
			if (!KnightsTour
			  (board, (xCoor + 2), (yCoor - 1), xSize, ySize,
			  (moveNum + 1)))
			     if (!KnightsTour
			      (board, (xCoor + 1), (yCoor - 2), xSize, ySize,
			      (moveNum + 1))) {
			      board[xCoor][yCoor] = xSize * ySize;
 return FALSE;
 }

 moveNum = 0;
 return TRUE;
}