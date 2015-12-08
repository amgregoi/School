#include <stdio.h>

int main ( int argc, char *argv[] )
{
    if ( argc != 2 ) /* argc should be 2 for correct execution */
    {
        /* We print argv[0] assuming it is the program name */
        printf( "usage: %s filename\n\n", argv[0] );
    }
    else 
    {
        // We assume argv[1] is a filename to open
        FILE *file = fopen( argv[1], "r" );

        /* fopen returns the NULL pointer on failure */
        if ( file == NULL )
        {
            printf( "Could not open file %s\n\n", argv[1] );
        }
        else 
        {
            char x;
            /* read one character at a time from file, stopping at EOF */
            while  ( ( x = fgetc( file ) ) != EOF )
            {
                printf( "%c", x );
            }
            fclose( file );
        }
    }
    return 0;
}

