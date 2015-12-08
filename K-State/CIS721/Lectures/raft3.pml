mtype = {Cop, Criminal, Mom, Dad, Girl1, Girl2, Boy1, Boy2, Boat};

#define DONE (r[Cop] == 1 && r[Criminal] == 1 && \
              r[Mom] == 1 && r[Dad] == 1 && \
              r[Girl1] == 1 && r[Girl2] == 1 && \
              r[Boy1] == 1 && r[Boy2] == 1 && r[Boat] == 1)

#define CriminalBeBad (r[Criminal] != r[Cop] && \
              (r[Criminal] == r[Mom] || r[Criminal] == r[Dad] || \
               r[Boy1] == r[Criminal] || r[Boy2] == r[Criminal] || \
               r[Girl1] == r[Criminal] || r[Girl2] == r[Criminal]))
#define BoyNotSafe ( (r[Boy1] == r[Mom] || r[Boy2] == r[Mom]) && r[Mom]!=r[Dad] )
#define GirlNotSafe ( (r[Girl1] == r[Dad] || r[Girl2] == r[Dad]) && r[Mom]!=r[Dad] )

mtype prev_dr = 0;
mtype prev_pass = 0;
show mtype driver = 0;
show mtype passenger = 0;

inline printMove(driver, passenger, boat)
{
    if
    :: boat == 0 ->
        if
        :: passenger == 0 -> printf("%e goes across alone.\n", driver);
        :: else -> printf("%e and %e go across.\n", driver, passenger);
        fi;
    :: else ->
        if
        :: passenger == 0 -> printf("%e goes back alone.\n", driver);
        :: else -> printf("%e and %e go back.\n", driver, passenger);
        fi;
    fi;
}

inline update_r()
{
    r[driver] = 1 - r[driver];
    if
    :: passenger != 0 -> r[passenger] = 1 - r[passenger];
    :: else -> skip;
    fi;
    r[Boat] = 1 - r[Boat];
}

inline move(driver, pass)
{
	printMove(driver, pass, r[Boat]);
    if
    :: (driver == prev_dr && pass == prev_pass) -> printf("Don't make same move.\n");
    :: else ->
        update_r();
        if
        :: (CriminalBeBad || BoyNotSafe || GirlNotSafe) -> printf("Bad Move - undo.\n"); update_r();
        :: else -> prev_dr = driver; prev_pass = pass;
        fi;
    fi;
}

/* global array for positions, initially all 0 = not crossed yet */
show int r[10];
/* mtypes are assigned from 1, arrays are indexed from 0, so r[0] is not used */

init {
    do
        /* move Cop (with anyone or alone) */
        :: r[Cop] == r[Boat] -> driver = Cop;
            if
            :: r[Criminal] == r[Boat] -> passenger = Criminal
            :: r[Mom] == r[Boat] -> passenger = Mom
            :: r[Dad] == r[Boat] -> passenger = Dad
            :: r[Boy1] == r[Cop] -> passenger = Boy1
            :: r[Boy2] == r[Cop] -> passenger = Boy2
            :: r[Girl1] == r[Cop] -> passenger = Girl1
            :: r[Girl2] == r[Cop] -> passenger = Girl2
            :: skip -> passenger = 0 /* no passenger */
            fi;
            move(driver, passenger);
        /* move Dad (with a Boy or with Mom or alone) */
        :: r[Dad] == r[Boat] -> driver = Dad;
            if
            :: r[Mom] == r[Boat] -> passenger = Mom
            :: r[Boy1] == r[Dad] -> passenger = Boy1
            :: r[Boy2] == r[Dad] -> passenger = Boy2	
            :: skip -> passenger = 0
            fi;
            move(driver, passenger);
        /* move Mom (with a Girl or alone) */
        :: r[Mom] == r[Boat] -> driver = Mom;
            if
            :: r[Girl1] == r[Mom] -> passenger = Girl1
            :: r[Girl2] == r[Mom] -> passenger = Girl2
            :: skip -> passenger = 0
            fi;
            move(driver, passenger);
        :: DONE -> printf("SOLVED\n"); assert(0); break;
        :: else -> printf("WHAT?!\n"); assert(0); break; /* Should never happen! */
    od;
}





