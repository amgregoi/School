
def double(a):
    """returns a list  b  that holds all of  a's  values * 2 (see post)"""
    """{ pre  True
         post forall 0 <= i < len(a), b[i] == a[i] * 2
         return b
    }"""
    b = []
    x = 0
    """{ 1.OK forall 0 <= i < x, b[i] == a[i] * 2    foralli
         2.OK x == len(b)                 algebra
    }"""
    while x != len(a) :
        """{ invariant  (forall 0 <= i < x, b[i] == a[i] * 2) and (x == len(b))
             modifies x, b
        }"""
        b.append(a[x]*2)
        """{ 1.OK (forall 0 <= i < x, b[i] == a[i] * 2) and (x == len(b_old))  premise
             2.OK x == len(b_old)                         ande 1
             10.OK forall 0 <= i < x, b[i] == a[i] * 2    ande 1
             3.OK len(b) == len(b_old) + 1                 premise
             4.OK x == len(b)-1                                 algebra 2 3
             5.OK b[len(b)-1] == a[x]*2                    premise
             6.OK b[x] == a[x]*2                          subst 4 5
             7.OK forall 0 <= i < x+1, b[i] == a[i] * 2  foralli 10 6
             8.OK len(b) == x + 1                         algebra 4
             9.OK return 7 8
        }"""
        x = x + 1
        """{ 1.OK  forall 0 <= i < x_old +1, b[i] == a[i] * 2  premise
             2.OK  x == x_old +1                              premise
             3.OK forall 0 <= i < x, b[i] == a[i] * 2    subst 2 1
             4.OK len(b) == x_old + 1                       premise
             5.OK len(b) == x                             subst 2 4
             6.OK x == len(b)                             algebra 5
             #7.OK (forall 0 <= i < x, b[i] == a[i] * 2) and (x == len(b)) andi 3 6
             8. return 3 6
        }"""

    """{ 1.OK (forall 0 <= i < x, b[i] == a[i] * 2) and (x == len(b))  premise
         3.OK not(x != len(a))                        premise
         4.OK x == len(a)                            algebra
         6.OK forall 0 <= i < x, b[i] == a[i] * 2    ande 1
         5.OK forall 0 <= i < len(a), b[i] == a[i] * 2   subst 4 6
    }"""
    return b
