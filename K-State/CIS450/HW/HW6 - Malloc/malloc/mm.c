/*
 * mm-naive.c - The fastest, least memory-efficient malloc package.
 * 
 * In this naive approach, a block is allocated by simply incrementing
 * the brk pointer.  A block is pure payload. There are no headers or
 * footers.  Blocks are never coalesced or reused. Realloc is
 * implemented directly using mm_malloc and mm_free.
 *
 * NOTE TO STUDENTS: Replace this header comment with your own header
 * comment that gives a high level description of your solution.
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>


#include "mm.h"
#include "memlib.h"

/*********************************************************
 * NOTE TO STUDENTS: Before you do anything else, please
 * provide your team information in the following struct.
 ********************************************************/
team_t team = {
    /* Team name */
    "AGDP",
    /* First member's full name */
    "Andy Gregoire",
    /* First member's email address */
    "amgregoi@ksu.edu",
    /* Second member's full name (leave blank if none) */
    "David Parker",
    /* Second member's email address (leave blank if none) */
    "dparker@ksu.edu"
};

/* single word (4) or double word (8) alignment */
#define ALIGNMENT 8

/* the following defines were borrowed from this pdf, Changed some names to make it more clear in my mind
http://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=7&ved=0CGMQFjAG&url=http%3A%2F%2Fciteseerx.ist.psu.edu%2Fviewdoc%2Fdownload%3Fdoi%3D10.1.1.138.4401%26rep%3Drep1%26type%3Dpdf&ei=7xmgUPKMF4K89QTPx4CwAQ&usg=AFQjCNGvmsua0jsqt38wSW4_at6Su168Vw&sig2=wogi3_Lfpa090muHe7NnMQ 
*/
/* rounds up to the nearest multiple of ALIGNMENT */	
#define READ(p)       (*(int *)(p))				//read word  at p
#define WRITE(p, val)  (*(int *)(p) = (val))	//write word at p
#define GET_SIZE(p)  (READ(p) & ~0x7)
#define HDRP(bp)       ((int *)(bp) - 2) //address of block header

static int* heap; //global ptr to heap
/* 
 * mm_init - initialize the malloc package.
 */
int mm_init(void)
{
    if((heap = mem_sbrk(48)) == (void *) -1) return -1;
	//list of heap sizes
	WRITE(heap, 0);		//when size is <= 128;
	WRITE(heap+1, 0);	//256
	WRITE(heap+2, 0);	//512
	WRITE(heap+3, 0);	//1024
	WRITE(heap+4, 0);	//2048
	WRITE(heap+5, 0);	//4096
	WRITE(heap+6, 0);	//8192
	WRITE(heap+7, 0);	//16384
	WRITE(heap+8, 0);	//32768
	WRITE(heap+9, 0);	//65536
	return 0;
	/*
	for(int i =0; i<=9; i++)
	{
		(*(int *)(p) = (val))
	}
	*/
}

/* 
 * mm_malloc - Allocate a block by incrementing the brk pointer.
 *     Always allocate a block whose size is a multiple of the alignment.
 */
void *mm_malloc(size_t size)
{
	int loc=-1;
	int** ptr;
	
	// set ind and size for heap, not very flexible but seemed to have the best performance for the test traces.
	if(size <=128) {loc = 0;size = 128;}
	else if(size <=256)  {loc = 1; size = 256;}
	else if(size <=512)  {loc = 2; size = 512;}
	else if(size <=1024) {loc = 3; size = 1024;}
	else if(size <=2048) {loc = 4; size = 2048;}
	else if(size <=4096) {loc = 5; size = 4096;}
	else if(size <=8192) {loc = 6; size = 8192;}
	else if(size <=16384){loc = 7; size = 16384;}
	else if(size <=32768){loc = 8; size = 32768;}
	else if(size <=65536){loc = 9; size = 65536;}
	
	//sets ptr to correct spot in heap QW
	ptr = *(heap + loc);
	if(!ptr)
	{
		if((ptr = mem_sbrk(size + ALIGNMENT)) == (void*) -1)
			return NULL;
		//fills spot in heap
		WRITE(ptr, size);
	}
	else
		*((int**) heap+loc) = (int*)*(ptr+1);
	
	//returns ptr to heap
	return (void*) ((int*) ptr+2);	
}

/*
 * mm_free - Freeing a block does nothing.
 */
void mm_free(void *ptr)
{
	int loc = -1;	//sets loc to -1 - default
	int* fptr;		
	
	//case statement - set correct loc based on ptr size
	switch(GET_SIZE(HDRP(ptr)))
	{
		case 128: loc = 0; break;
		case 256: loc = 1; break;
		case 512: loc = 2; break;
		case 1024: loc = 3; break;
		case 2048: loc = 4; break;
		case 4096: loc = 5; break;
		case 8192: loc = 6; break;
		case 16384: loc = 7; break;
		case 32768: loc = 8; break;
		case 65536: loc = 9; break;
		default: break;
	}
	//end statement
	fptr = (heap + loc);
	if(! *fptr)
		*((int*) ptr -1) = 0;	//set 1st block to 0
	else
		*((int*) ptr -1) = *fptr;	// points to previous first in list
	*((int**) fptr) = (int*) ptr-2; // point to now free block
}

/*
 * mm_realloc - Implemented simply in terms of mm_malloc and mm_free
 */
void *mm_realloc(void *ptr, size_t size)
{
    void *oldPtr = ptr;
    void *newPtr;
    size_t copySize;
	
	copySize = *(size_t *)((int *) oldPtr - 2);
	//if size is larger than current block call mm_malloc and mm_free to return new block
    if (size > copySize) 
	{
		copySize = size;	//possible get rid of this?
		newPtr = mm_malloc(size);
		
		if (newPtr == NULL)
			return NULL;
		
		memcpy(newPtr, oldPtr, copySize);
		mm_free(oldPtr);
		return newPtr;   
    } 
	else //else return old block 
		return oldPtr;			
}















