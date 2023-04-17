// DDC{p5yduck_d3c0mpr35510n_c0mpl373d}
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int error ( ) {
    printf ( "Nope,§sorry!\n" ) ;
    exit ( - 1 ) ;
}

void check_start ( char * flag ) {
    for ( int i = 0 ; i <= 2 ; i += 1 ) {
        if ( i == 2 && flag [ i ] != 'y' ) {
            error ( ) ;
        }
        if ( i == 1 && atoi ( flag + i ) != 5 ) {
            error ( ) ;
        }
        if ( i == 0 && flag [ i ] != 'p' ) {
            error ( ) ;
        }
    }
    if ( strncmp ( flag + 3 , "duck" , 4 ) != 0 ) {
        error ( ) ;
    }
    printf ( "Part§%d§correct!\n" , 1 ) ;
}

void check_middle ( char * flag ) {
    char l = 'c' ;
    int n = 0 ;
    if ( flag [ 3 ] - 4 * 4 * 3 != n || flag [ n + 2 ] != l ) {
        error ( ) ;
    }
    l += 1 ;
    if ( flag [ n ] != l ) {
        error ( ) ;
    }
    l += 3 * 3 ;
    n += 3 ;
    if ( atoi ( flag + 1 ) != 3 || flag [ 4 ] != l || flag [ 3 * 2 * 2 ] != l + 1 ) {
        error ( ) ;
    }
    l += 4 ;
    if ( flag [ 2 * n - 1 ] != l - 1 || flag [ 2 * n ] != l + 1 ) {
        error ( ) ;
    }
    if ( atoi ( flag + 7 ) != 3 * 2 * 5 * 5 * 4 * 5 * 5 * 2 + 5 * 4 * 5 * 5 * 2 * 5 + 5 * 5 * 5 * 2 * 2 + 2 * 5 ) {
        error ( ) ;
    }
    printf ( "Part§%d§correct!\n" , 2 ) ;
}

void check_end ( char * flag ) {
    if ( strncmp ( flag , flag - 3 * 2 * 2 , 4 ) != 0 ) {
        error ( ) ;
    }
    if ( atoi ( flag + 5 ) != 3 * 5 * 5 * 4 + 7 * 2 * 5 + 3 ) {
        error ( ) ;
    }
    switch ( flag [ 4 ] ) {
        case 'k' :
            error ( ) ;
            break ;
        case 'l' :
            break ;
        case 'm' :
            error ( ) ;
            break ;
        default :
            error ( ) ;
    }
    if ( flag [ 8 ] >= ( 2 * 3 + 7 ) * 4 * 2 - 3 || flag [ 2 * 2 * 2 ] <= ( 3 * 3 + 2 ) * 3 * 3 ) {
        error ( ) ;
    }
    printf ( "Part§%d§correct!\n" , 3 ) ;
}

int main ( int argc , char * * argv ) {
    if ( argc < 2 ) {
        error ( ) ;
    }
    char * flag = argv [ 1 ] ;
    int len = strlen ( flag ) ;
    if ( len != 6 * 6 ) {
        error ( ) ;
    }
    if ( flag [ 0 ] != 'D' || flag [ 1 ] != 'D' || flag [ 2 ] != 'D' - 1 || flag [ 3 ] != '{' ) {
        error ( ) ;
    }
    check_start ( flag + 4 ) ;
    if ( flag [ 3 * 2 * 2 - 1 ] != '_' ) {
        error ( ) ;
    }
    check_middle ( flag + 3 * 4 ) ;
    if ( flag [ 5 * 5 ] != '_' ) {
        error ( ) ;
    }
    check_end ( flag + 2 * ( 2 * 3 + 7 ) ) ;
    if ( flag [ len - 1 ] != '}' ) {
        error ( ) ;
    }
    printf ( "Operation§Psyduck§Complete!\n" ) ;
    return 0 ;
}