
def double(a):
    """returns a list  b  that holds all of  a's  values * 2 (see post)"""
    """{ pre  True
         post forall 0 <= i < len(a), b[i] == a[i] * 2
         return b
    }"""
    b = []
    x = 0
    """{ 1. forall 0 <= i < x, b[i] == a[i] * 2    foralli
         2. x == len(b)                 algebra
    }"""
    while x != len(a) :
        """{ invariant  (forall 0 <= i < x, b[i] == a[i] * 2) and (x == len(b))
             modifies x, b
        }"""
        b.append(a[x]*2)
        """{ 1. (forall 0 <= i < x, b[i] == a[i] * 2) and (x == len(b_old))  premise
             2. x == len(b_old)                         ande 1
             10. forall 0 <= i < x, b[i] == a[i] * 2    ande 1
             3. len(b) == len(b_old) + 1                 premise
             4. x == len(b)-1                                 algebra 2 3
             5. b[len(b)-1] == a[x]*2                    premise
             6. b[x] == a[x]*2                          subst 4 5
             7. forall 0 <= i < x+1, b[i] == a[i] * 2  foralli 10 6
             8. len(b) == x + 1                         algebra 4
             9. return 7 8
        }"""
        x = x + 1
        """{ 1.  forall 0 <= i < x_old +1, b[i] == a[i] * 2  premise
             2.  x == x_old +1                              premise
             3. forall 0 <= i < x, b[i] == a[i] * 2    subst 2 1
             4. len(b) == x_old + 1                       premise
             5. len(b) == x                             subst 2 4
             6. x == len(b)                             algebra 5
             #7. (forall 0 <= i < x, b[i] == a[i] * 2) and (x == len(b)) andi 3 6
             8. return 3 6
        }"""

    """{ 1. (forall 0 <= i < x, b[i] == a[i] * 2) and (x == len(b))  premise
         3. not(x != len(a))                        premise
         4. x == len(a)                            algebra
         6. forall 0 <= i < x, b[i] == a[i] * 2    ande 1
         5. forall 0 <= i < len(a), b[i] == a[i] * 2   subst 4 6
    }"""
    return b
