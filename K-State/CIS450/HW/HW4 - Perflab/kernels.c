/********************************************************
 * Kernels to be optimized for the CS:APP Performance Lab
 ********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include "defs.h"

/* 
 * Please fill in the following team struct 
 */
team_t team = {
    "AGDP",              /* Team name */

    "Andy Gregoire",     /* First member full name */
    "amgregoi@k-state.edu",  /* First member email address */
};

/***************
 * ROTATE KERNEL
 ***************/

/******************************************************
 * Your different versions of the rotate kernel go here
 ******************************************************/

/* 
 * naive_rotate - The naive baseline version of rotate 
 */
char naive_rotate_descr[] = "naive_rotate: Naive baseline implementation";
void naive_rotate(int dim, pixel *src, pixel *dst) 
{
    int i, j;	

    for (i = 0; i < dim; i++)
	for (j = 0; j < dim; j++)
	    dst[RIDX(dim-1-j, i, dim)] = src[RIDX(i, j, dim)];
}

/* 
 * rotate - Your current working version of rotate
 * IMPORTANT: This is the version you will be graded on
 */
 /*
char rotate1_descr[] = "rotate: Current working version";
void rotate1(int dim, pixel *src, pixel *dst) 
{
			 // 1) blocked into 16's, 2) unwrap the RIDIX calls 
	int size = dim * dim - dim;
	int k, j;
	for(k = 0; k < dim; k += 16)
	{
		int temp = dim * k;
		for(j = 0; j < dim; j++)
		{
			int num = size - j * dim;
			int i = temp + j;
			dst[num + k] = src[i];
			dst[num + (k + 1)] = src[i += dim];
			dst[num + (k + 2)] = src[i += dim];
			dst[num + (k + 3)] = src[i += dim];
			dst[num + (k + 4)] = src[i += dim];
			dst[num + (k + 5)] = src[i += dim];
			dst[num + (k + 6)] = src[i += dim];
			dst[num + (k + 7)] = src[i += dim];
			dst[num + (k + 8)] = src[i += dim];
			dst[num + (k + 9)] = src[i += dim];
			dst[num + (k + 10)] = src[i += dim];
			dst[num + (k + 11)] = src[i += dim];
			dst[num + (k + 12)] = src[i += dim];
			dst[num + (k + 13)] = src[i += dim];
			dst[num + (k + 14)] = src[i += dim];
			dst[num + (k + 15)] = src[i += dim];

		}
	}
}
*/
char rotate_descr[] = "rotate1: Current working version";
void rotate(int dim, pixel *src, pixel *dst){
    int i, j;											// initialize i,j for loops
    int dst_base = (dim-1)*dim;							// initialize dst_base
    dst += dst_base;									
    for (i = 0; i < dim; i+=16){ 						// 16 blocks
            for (j = 0; j < dim; j++){ 					// of 1 operation
                *dst=*src;								// sets dst = src					- repeats 15 times
                src+=dim;								// increments src by value dim
                dst++;									// incrememnt dst by 1

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;	
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;
                src+=dim;
                dst++;

                *dst=*src;

                    src++;
                    src -= (dim*16)-dim;
                    dst-=15+dim;
            }
            dst+=dst_base+dim;
            dst+=16;
            src += 15*dim;

        }
}

/*********************************************************************
 * register_rotate_functions - Register all of your different versions
 *     of the rotate kernel with the driver by calling the
 *     add_rotate_function() for each test function. When you run the
 *     driver program, it will test and report the performance of each
 *     registered test function.  
 *********************************************************************/

void register_rotate_functions() 
{
    add_rotate_function(&naive_rotate, naive_rotate_descr);   
    add_rotate_function(&rotate, rotate_descr);   
	//add_rotate_function(&rotate1, rotate1_descr);
    /* ... Register additional test functions here */
}


/***************
 * SMOOTH KERNEL
 **************/

/***************************************************************
 * Various typedefs and helper functions for the smooth function
 * You may modify these any way you like.
 **************************************************************/

/* A struct used to compute averaged pixel value */
typedef struct {
    int red;
    int green;
    int blue;
    int num;
} pixel_sum;

/* Compute min and max of two integers, respectively */
static int min(int a, int b) { return (a < b ? a : b); }
static int max(int a, int b) { return (a > b ? a : b); }

/* 
 * initialize_pixel_sum - Initializes all fields of sum to 0 
 */
static void initialize_pixel_sum(pixel_sum *sum) 
{
    sum->red = sum->green = sum->blue = 0;
    sum->num = 0;
    return;
}

/* 
 * accumulate_sum - Accumulates field values of p in corresponding 
 * fields of sum 
 */
static void accumulate_sum(pixel_sum *sum, pixel p) 
{
    sum->red += (int) p.red;
    sum->green += (int) p.green;
    sum->blue += (int) p.blue;
    sum->num++;
    return;
}

/* 
 * assign_sum_to_pixel - Computes averaged pixel value in current_pixel 
 */
static void assign_sum_to_pixel(pixel *current_pixel, pixel_sum sum) 
{
    current_pixel->red = (unsigned short) (sum.red/sum.num);
    current_pixel->green = (unsigned short) (sum.green/sum.num);
    current_pixel->blue = (unsigned short) (sum.blue/sum.num);
    return;
}

/* 
 * avg - Returns averaged pixel value at (i,j) 
 */
static pixel avg(int dim, int i, int j, pixel *src) 
{
    int ii, jj;
    pixel_sum sum;
    pixel current_pixel;

    initialize_pixel_sum(&sum);
    for(ii = max(i-1, 0); ii <= min(i+1, dim-1); ii++) 
	for(jj = max(j-1, 0); jj <= min(j+1, dim-1); jj++) 
	    accumulate_sum(&sum, src[RIDX(ii, jj, dim)]);

    assign_sum_to_pixel(&current_pixel, sum);
    return current_pixel;
}

/******************************************************
 * Your different versions of the smooth kernel go here
 ******************************************************/

/*
 * naive_smooth - The naive baseline version of smooth 
 */
char naive_smooth_descr[] = "naive_smooth: Naive baseline implementation";
void naive_smooth(int dim, pixel *src, pixel *dst) 
{
    int i, j;

    for (i = 0; i < dim; i++)
	for (j = 0; j < dim; j++)
	    dst[RIDX(i, j, dim)] = avg(dim, i, j, src);
}

/*
 * smooth - Your current working version of smooth. 
 * IMPORTANT: This is the version you will be graded on
 */
char smooth_descr[] = "smooth: Current working version";
static  void add_row(pixel_sum *sums, int dim, pixel *row) {
	int i;															// i - initialized for 'for loop'
	pixel *one = row-1;												// pixel before row (row-1)
	pixel *two = row+1;												// pixel after row (row+1)
	pixel_sum *total = sums++;;		 								// total of three added together (red, green, blue)
	
	// calculates left edge of current row
	total->red = row->red + two->red;								// adds red of row & row+1 into total->red			
	total->green = row->green + two->green;							// adds green of row & row+1 into total->green	
	total->blue = row->blue + two->blue;							// adds blue of row & row+1 into total->blue
	row++;															// increment row
		
	//calculates middle of current row
	for (i=1; i<dim-1; i++) {
		one = row-1;												// update one for middle row
		two = row+1;												// update two for middle row
		total = sums++;												// increment total
		total->red = one->red + row->red + two->red;				// adds red (row-1)+row+(row+1) into total->red
		total->green = one->green + row->green + two->green;		// adds green (row-1)+row+(row+1) into total->green
		total->blue = one->blue + row->blue + two->blue;			// adds blue (row-1)+row+(row+1) into total->blue
		row++;
	}
	// calculates the right edge of current row
	one = row-1;						
	sums->red = one->red + row->red;								// adds red of row & row+1 into total->red (
	sums->green = one->green + row->green;							// adds green of row & row+1 into total->green
	sums->blue = one->blue + row->blue;								// adds blue of row & row+1 into total->blue
}

// used to averages edges
static  void avg_edge(int div, pixel *dst, pixel_sum *one, pixel_sum *two) {
	dst->red = (one->red + two->red)/div;							// averages red into dst->red (destination pixel)
	dst->green = (one->green + two->green)/div;						// avg green into dst->green
	dst->blue = (one->blue + two->blue)/div;						// avg blue into dst->blue
}

// used to average mid
static  void avg_mid(int div, pixel *dst, pixel_sum *one, pixel_sum *two, pixel_sum *three) {
	dst->red = (one->red + two->red + three->red)/div;				// averages red into dst->red (destination pixel)
	dst->green = (one->green + two->green + three->green)/div;		// avg green into dst->green
	dst->blue = (one->blue + two->blue + three->blue)/div;			// avg blue into dst->blue
}

/*	Keep track of pixel dividers for avg
	top/bot - edge  -> divide by 4
	top/bot - mid	-> divide by 6
	mid - edge		-> divide by 6
	mid - mid		-> divide by 9
*/
void smooth(int dim, pixel *src, pixel *dst) {
	pixel_sum *row_sums = malloc(3*dim*sizeof(pixel_sum));
	pixel_sum *pOne = row_sums;										// initialized now for top row
	pixel_sum *pTwo = pOne+dim;										// initialized now for top row
	pixel_sum *pThree;												// initialized later, only needed for mid rows
	int i, j;														// initialized for loops

	add_row(pOne, dim, src);
	add_row(pTwo, dim, src+dim);
	
	// calculate top row
	avg_edge(4, dst++, pOne++, pTwo++);								// average corner of top row
	for (i=1; i<dim-1; i++)
		avg_edge(6, dst++, pOne++, pTwo++);							//averages mid of top row
	avg_edge(4, dst++, pOne, pTwo);									// averages other corner of top row

	// calculate mid row
	for (i=1; i<dim-1; i++) {
		pOne = row_sums+((i-1)%3)*dim;								// update pOne for mid rows
		pTwo = row_sums+(i%3)*dim;									// updates pTwo for mid rows
		pThree = row_sums+((i+1)%3)*dim;							// initialize pThree for mid rows
		add_row(pThree, dim, src+(i+1)*dim);						// calls add row
		avg_mid(6, dst++, pOne++, pTwo++, pThree++);				// averages top edge of middle rows
		for (j=1; j<dim-1; j++)	
			avg_mid(9, dst++, pOne++, pTwo++, pThree++);			//	averages middle of middle rows
		avg_mid(6, dst++, pOne, pTwo, pThree);						// averages bottom edge of middle rows
	}

	// calculate bottom row
	pOne = row_sums+((i-1)%3)*dim;									// update pOne for bottom row
	pTwo = row_sums+(i%3)*dim;										// update pTwo for bottom row
	avg_edge(4, dst++, pOne++, pTwo++);								// averages corner of bottom row
	for (i=1; i<dim-1; i++)
		avg_edge(6, dst++, pOne++, pTwo++); 						// averages mid of bottom row
	avg_edge(4, dst, pOne, pTwo);									// averages other corner bottom row
}


/********************************************************************* 
 * register_smooth_functions - Register all of your different versions
 *     of the smooth kernel with the driver by calling the
 *     add_smooth_function() for each test function.  When you run the
 *     driver program, it will test and report the performance of each
 *     registered test function.  
 *********************************************************************/

void register_smooth_functions() {
    add_smooth_function(&smooth, smooth_descr);
    add_smooth_function(&naive_smooth, naive_smooth_descr);
    /* ... Register additional test functions here */
}

