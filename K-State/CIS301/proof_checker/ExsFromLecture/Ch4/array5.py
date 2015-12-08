

#a = [] 

def square():
    """Updates global array  a  in place so that each of its ints are squared"""
    """{ pre  True
         post forall 0 <= i < len(a), a[i] == a_in[i] * a_in[i]
    }"""
    global a
    x = 0
    """{ 1. forall 0 <= _i < len(a), a[_i] == a_in[_i]  premise
         2. forall 0 <= i < len(a), a[i] == a_in[i]  substindex 1
         3. x == 0                                   premise
         4. forall x <= i < len(a), a[i] == a_in[i]  subst 3 2
         5. forall 0 <= i < x, a[i] == a_in[i] * a_in[i]   foralli 3
         5. return 4 5
    }"""
    while x != len(a) :
        """{ invariant  (forall 0 <= i < x, a[i] == a_in[i] * a_in[i]) and (forall x <= i < len(a), a[i] == a_in[i])
             modifies x, a
        }"""
        """{ 1. (forall 0 <= i < x, a[i] == a_in[i] * a_in[i]) and (forall x <= i < len(a), a[i] == a_in[i])     premise
             2. forall 0 <= i < x, a[i] == a_in[i] * a_in[i]    ande 1
             3. forall x <= i < len(a), a[i] == a_in[i]         ande 1
             4. return 2 3
        }"""
        assert x >= 0  # this is actually an invariant
        assert x < len(a)  # this is actually an invariant
        a[x] = a[x] * a[x]
        """{ 1.  a[x] == a_old[x] * a_old[x]                        premise
             2. forall 0 <= i < x, a[i] == (a_in[i] * a_in[i])      premise
             3. forall x <= i < len(a_old), a_old[i] == a_in[i]     premise
             4. a_old[x] == a_in[x]                                 foralle x 3
             5. a[x] == a_in[x] * a_in[x]                           subst 4 1
             6. forall 0 <= i < (x+1), a[i] == (a_in[i] * a_in[i])  foralli 2 5
             7. forall (x+1) <= i < len(a), a[i] == a_in[i]         premise
             8. return 6 7
        }"""
        x = x + 1
        """{ 1. forall 0 <= i < (x_old+1), a[i] == (a_in[i] * a_in[i]) premise
             2. forall (x_old + 1) <= i < len(a), a[i] == a_in[i]     premise
             3. x == x_old + 1                                       premise
             4. forall 0 <= i < x, a[i] == (a_in[i] * a_in[i])       subst 3 1
             5. forall x <= i < len(a), a[i] == a_in[i]              subst 3 2
             6. return 4 5
        }"""

    """{ 1. (forall 0 <= i < x, a[i] == (a_in[i] * a_in[i])) and (forall x <= i < len(a), (a[i] == a_in[i]))                       premise
         2. not (x != len(a))                      premise
         3. x == len(a)                            algebra 2
         4. forall 0 <= i < x, a[i] == (a_in[i] * a_in[i])   ande 1
         5. forall 0 <= i < len(a), a[i] == (a_in[i] * a_in[i])   subst 3 4
    }"""

