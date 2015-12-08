#include <stdio.h>
void life(int *this, int *new)
{
	unsigned bitmap;
	int *next, *prev;
	int x, y;
	static enum {
		DEAD, LIVE
	} state[1 << 9];

	if(state[007] == 0) {
		for(bitmap = 0; bitmap < 1<<9; bitmap++) {
			for(x = y = 0; y < 9; y++)
				if(bitmap & 1<<y)
					x += 1;
			if(bitmap & 020) {
				if(x == 2 || x == 3)
					state[bitmap] = LIVE;
				else
					state[bitmap] = DEAD;
			} else {
				if(x == 3)
					state[bitmap] = LIVE;
				else
					state[bitmap] = DEAD;
			}
		}
	}

	prev = next = this;
	bitmap = 0;
	*new = 0;
	for(;;) {
		/* did we write an X co-ordinate? */
		if(*new < 0)
			new++;
		if(prev == next) {
			/* start a new group of rows */
			if(*next == 0) {
				*new = 0;
				return;
			}
			y = *next++ + 1;
		} else {
			/* move to next row and work out which ones to scan */
			if(*prev == y--)
				prev++;
			if(*this == y)
				this++;
			if(*next == y-1)
				next++;
		}
		/* write new row co-ordinate */
		*new = y;
		for(;;) {
			/* skip to the leftmost cell */
			x = *prev;
			if(x > *this)
				x = *this;
			if(x > *next)
				x = *next;
			/* end of line? */
			if(x >= 0)
				break;
			for(;;) {
				/* add a column to the bitmap */
				if(*prev == x) {
					bitmap |= 0100;
					prev++;
				}
				if(*this == x) {
					bitmap |= 0200;
					this++;
				}
				if(*next == x) {
					bitmap |= 0400;
					next++;
				}
				/* what does this bitmap indicate? */
				if(state[bitmap] == LIVE)
					*++new = x - 1;
				else if(bitmap == 000)
					break;
				/* move right */
				bitmap >>= 3;
				x += 1;
			}
		}
	}
}

int main(){
	int *x, *y = 0;
	life(x, y);
}



