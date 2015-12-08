/*
 * mm-awesome.c - The fastest, awesomest malloc package.
 * 
 * This package uses segmented free lists to keep track of
 * free blocks of memory. Coalescing blocks is delayed until
 * no free blocks are availble. 
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>

#include "mm.h"
#include "memlib.h"

#define DEBUG 1

/*********************************************************
 * NOTE TO STUDENTS: Before you do anything else, please
 * provide your team information in the following struct.
 ********************************************************/
team_t team = {
    /* Team name (id1+id2)*/
    "bpan+andylei",
    /* First member's full name */
    "Bohao Pan",
    /* First member's email address */
    "bpan@fas.harvard.edu",
    /* Second member's full name (leave blank if none) */
    "Andy Lei",
    /* Second member's email address (leave blank if none) */
    "andylei@fas.harvard.edu"
};

/* single word (4) or double word (8) alignment */
#define ALIGNMENT 8

/* rounds up to the nearest multiple of ALIGNMENT */
#define ALIGN(size) (((size) + (ALIGNMENT-1)) & ~0x7)


#define SIZE_T_SIZE (ALIGN(sizeof(size_t)))

/* minimum size for a block */
#define MIN_BLOCK_SIZE (SIZE_T_SIZE * 3)

/* cutoff for exactly sized lists */
#define MIN_APPROX_SIZE (0x100)

// block traversal macros
#define PAYLOAD(block_header) ((header **)((char *) block_header + SIZE_T_SIZE))
#define HEADER(payload_ptr) ((header *)((char *) payload_ptr - SIZE_T_SIZE))
#define NEXT_FREE(block_header) (*PAYLOAD(block_header))
#define PREV_FREE(block_header) (*(PAYLOAD(block_header)+1))

#define LEFT_CHILD(block_header) (NEXT_FREE(block_header))
#define RIGHT_CHILD(block_header) (NEXT_FREE(block_header))

#define GET_SIZE(block_header) (*block_header & ~0x1)
#define NEXT(block_header) ((header *)((char *) block_header + GET_SIZE(block_header)))


#define MARK_ALLOC(block_header) (*block_header = *block_header | 0x1)
#define MARK_FREE(block_header) (*block_header = *block_header - 1)

/* return false if its a free block */
#define IS_ALLOCED(block_header) (*block_header % 2)
#define IS_FREE(block_header) (~IS_ALLOCED(block_header))

typedef size_t header;

void print_all();

/* =========  Global Variables  ========= */

/* 
 * the pointers to our segmented free lists, where
 * segments[n] contains memory blocks with size between
 * 2^n and 2^(n+1). the headers of the blocks are size_t's
 * with least significant bit 0 if free and 1 if allocated.
 */
header * segments[32];

/* 
 * mem_head points to a "free" block that never gets allocated.
 *  the head of the free list is always free (to make it easier to
 *  deal with doubly linked list related issues).
 */
header * mem_head;
header * end;

/* 
 * mm_init - initialize the malloc package.
 */
int mm_init(void)
{
    mem_head = malloc(ALIGN(1024) * 3);
    *mem_head = ALIGN(1024);
    NEXT_FREE(mem_head) = NEXT(mem_head);
    PREV_FREE(mem_head) = NULL;
    
    header * mem1 = NEXT(mem_head);
    *mem1 = ALIGN(1024);
    NEXT_FREE(mem1) = NEXT(mem1);
    PREV_FREE(mem1) = mem_head;
    
    header * mem2 = NEXT(mem1);
    *mem2 = ALIGN(1024);
    NEXT_FREE(mem2) = NULL;
    PREV_FREE(mem2) = mem1;
    
    end = (header *)(((char *)mem_head) + ALIGN(1024) * 3);
    return 0;

	// setup the exact segments


	// setup the approx segments

}
/************  Doubly Linked List Functions  *************/

/*
 * Remove node from doubly linked list
 */
void remove_from_llist(header * node)
{
    header * nextfree = NEXT_FREE(node);
    header * prevfree = PREV_FREE(node);
    
	if(prevfree != NULL)
		NEXT_FREE(prevfree) = nextfree;
	if(nextfree != NULL)
		PREV_FREE(nextfree) = prevfree;
}

/*
 * Add node to a doubly linked list after after
 */
void add_to_llist(header * node, header * after)
{
	header * next = NEXT_FREE(after);
	
	NEXT_FREE(after) = node;
	PREV_FREE(node) = after;
	
	NEXT_FREE(node) = next;
	if(next != NULL)
		PREV_FREE(next) = node;
}

/***********  Binary Tree Functions  **************
 *
 * our binary tree uses the convention that the left child has greater value
 * than the right child.  the right child may have value equal to parent.
 *
 */

/* push node into the tree at root */

void tree_push(header * node, header * root)
{
	
}

/* 
 * tree_pop() - find the smallest node w/ size > size and remove
 *  it from the tree.  return NULL if there are no nodes matching the
 *  criteria.
 */

header * tree_pop(header * root, size_t size)
{
	header * best = NULL;
	header * best_parent = NULL;
	header * cur = root;
	header * prev = root;
	
	// find the node
	if(*cur >= size)
		cur = RIGHT_CHILD(cur);
	else
		cur = LEFT_CHILD(cur);
	while(cur != NULL)
	{
		if(*cur == size)
		{
			best_parent = prev;
			best = cur;
			break;
		}
		if(*cur > size)
		{
			best_parent = prev;
			best = cur;
			prev = cur;
			cur = RIGHT_CHILD(cur);
		}
		else
		{
			prev = cur;
			cur = LEFT_CHILD(cur);
		}
	}
	
	if(best == NULL)
		return NULL;
	
	// remove it from the tree
	
	
	return best;
}


/*
 * Mark the block as allocated, possibly split the block, remove
 * the allocated block from the free list, and return a pointer to
 * the payload region of the allocated block.
 * Assumes that block is at least of size size.
 */
void * allocate(header * block, size_t size)
{
#ifdef DEBUG
	printf("Allocating %p, for size %lu", block, size);
#endif
    // split the block
	size_t split_size = *block - size;
    if(split_size >= MIN_BLOCK_SIZE)
    {
#ifdef DEBUG
		printf(", split size: %lu.\n", split_size);
#endif
		// split the block in two
        *block = size;
		header * split = NEXT(block); //second half of the split block
		*split = split_size;
#ifdef DEBUG
		print_all();
#endif
		
		// rebuild the linked list pointers to reflect
		header * next = NEXT_FREE(block);
		if(next != NULL)
			PREV_FREE(next) = split;
	
		// prev is guaranteed, since we never allocate the first element 
		//  of any free list
		NEXT_FREE(PREV_FREE(block)) = split;
		NEXT_FREE(split) = NEXT_FREE(block);
		
		printf("%p\n", PREV_FREE(split));
		printf("%p\n", PREV_FREE(block));
		PREV_FREE(split) = PREV_FREE(block);
    } else 
	{
#ifdef DEBUG
		printf(", no splitting.\n");
#endif
		remove_from_llist(block);
	}
	
    // mark the block as allocated
    MARK_ALLOC(block);
    
	// pointer to the payload
    return (void *) PAYLOAD(block);
}

/* 
 * coalesce() - Coalesces free memory until memory of size size is created
 *  at which point coalesce returns a pointer to a block with size at least
 *  size.  Assumes that size is already aligned.  Returns NULL if colaescing
 *  finishes without finding such a block.  If size is 0, then finishes
 *  coalescing and returns NULL.
 */
header * coalesce(size_t size)
{
#ifdef DEBUG
	printf("Running coalesce...\n");
#endif
	header * cur = NEXT(mem_head);
	header * next = NEXT(cur);
	while (next != NULL) {
		if (IS_FREE(cur) && IS_FREE(next)) {
#ifdef DEBUG
			printf("    coalescing %p and %p.\n", cur, next);		
#endif
			remove_from_llist(cur);
			remove_from_llist(next);
			
			*cur += *next;
			add_to_llist(cur, mem_head);
			if (size && *cur >= size)
				return cur;
		} 
		else 
		{
			cur = next;
		}
		next = NEXT(cur);
	}
	return NULL;
}

header * find_free(size_t size)
{
    header * mem = NEXT_FREE(mem_head);
    while(mem != NULL)
    {
        if(*mem >= size)
            return mem;
        mem = NEXT_FREE(mem);
    }
    
    return NULL;
}
/* 
 * mm_malloc - Allocate a block by incrementing the brk pointer.
 *     Always allocate a block whose size is a multiple of the alignment.
 */
void *mm_malloc(size_t size)
{
    size_t newsize = ALIGN(size + SIZE_T_SIZE);
    
    /* find a free block in the lists */
    header * block = find_free(newsize);
    if(block == NULL)
    {
		// coalesce, find a free block
		block = coalesce(newsize);
		
		// sbrk
        //if(block == NULL) sbrk();
    }
    
    void * ptr = allocate(block, newsize);
    return ptr;
}

/*
 * mm_free - Freeing a block
 */
void mm_free(void *ptr)
{
	header * block = HEADER(ptr);
#ifdef DEBUG
	printf("Freeing pointer at %p with header at %p, w/ size %lu\n", ptr, block, *block);
#endif
	MARK_FREE(block);
	add_to_llist(block, mem_head);
}

/*
 * mm_realloc - Implemented simply in terms of mm_malloc and mm_free
 */
void *mm_realloc(void *ptr, size_t size)
{
    void *oldptr = ptr;
    void *newptr;
    size_t copySize;
    
    newptr = mm_malloc(size);
    if (newptr == NULL)
      return NULL;
    copySize = *(size_t *)((char *)oldptr - SIZE_T_SIZE);
    if (size < copySize)
      copySize = size;
    memcpy(newptr, oldptr, copySize);
    mm_free(oldptr);
    return newptr;
}

void print_block(header * block)
{
	printf("%p | prev: %8p | next: %8p | size: %6u | allocated: %1lu\n", 
		   block, PREV_FREE(block), NEXT_FREE(block),
		   GET_SIZE(block), IS_ALLOCED(block)
	);
}

/*
 * print_all() - Prints every block in the memory structure
 */
void print_all()
{
    header * cur = mem_head;
    while(cur < end)
    {
        print_block(cur);
        cur = NEXT(cur);
    }
	printf("\n");
}

/*
 * print_free() - Prints all the free memory, in order
 */
void print_free(header * head)
{
	header * cur = NEXT_FREE(head);
	while(cur != NULL)
	{
		print_block(cur);
		cur = NEXT_FREE(cur);
	}
	printf("\n");
}

int main (int argc, const char * argv[]) {

    mm_init();
    print_all();
	
	void * omg = mm_malloc(300);
	print_all();
	void * omg2 = mm_malloc(1000);
	print_all();
	mm_free(omg);
	omg = mm_malloc(1000);
	print_all();
	mm_free(omg2);
	print_all();
	mm_free(omg);
	print_all();
}

