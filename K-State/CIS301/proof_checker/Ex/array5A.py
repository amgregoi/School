

a = [] 
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (a == [])
#PREMISES FOR NEXT LINE: 
# (a == [])

def square():
    """Updates global array  a  in place so that each of its ints are squared"""
    """{ pre  True
         post forall 0 <= i < len(a), a[i] == a_in[i] * a_in[i]
    }"""
    global a
    a_in = [ _v for _v in a ]
    #PREMISES FOR NEXT LINE: 
    # True
    # forall 0 <= _i < len(a), (a[_i] == a_in[_i])
    # (len(a) == len(a_in))
    x = 0
    #PREMISES FOR ATTACHED PROOF, IF ANY: 
    # (x == 0)
    # True
    # forall 0 <= _i < len(a), (a[_i] == a_in[_i])
    # (len(a) == len(a_in))
    """{ 1.OK forall 0 <= _i < len(a), a[_i] == a_in[_i]  premise
         2.OK forall 0 <= i < len(a), a[i] == a_in[i]  substindex 1
         3.OK x == 0                                   premise
         4.OK forall x <= i < len(a), a[i] == a_in[i]  subst 3 2
         5.OK forall 0 <= i < x, a[i] == a_in[i] * a_in[i]   foralli 3
         6.OK return 4 5
    }"""
    #PREMISES FOR NEXT LINE: 
    # forall x <= i < len(a), (a[i] == a_in[i])
    # forall 0 <= i < x, (a[i] == (a_in[i] * a_in[i]))
    while x != len(a) :
        """{ invariant  (forall 0 <= i < x, a[i] == a_in[i] * a_in[i]) and (forall x <= i < len(a), a[i] == a_in[i])
             modifies x, a
        }"""
        #PREMISES FOR LOOP BODY: 
        # (x != len(a))
        # (forall 0 <= i < x, (a[i] == (a_in[i] * a_in[i])) and forall x <= i < len(a), (a[i] == a_in[i]))
        """{ 1.OK (forall 0 <= i < x, a[i] == a_in[i] * a_in[i]) and (forall x <= i < len(a), a[i] == a_in[i])     premise
             2.OK forall 0 <= i < x, a[i] == a_in[i] * a_in[i]    ande 1
             3.OK forall x <= i < len(a), a[i] == a_in[i]         ande 1
             4.OK return 2 3
        }"""
        #PREMISES FOR NEXT LINE: 
        # forall 0 <= i < x, (a[i] == (a_in[i] * a_in[i]))
        # forall x <= i < len(a), (a[i] == a_in[i])
        assert x >= 0  # this is actually an invariant
        #PREMISES FOR NEXT LINE: 
        # (x >= 0)
        # forall 0 <= i < x, (a[i] == (a_in[i] * a_in[i]))
        # forall x <= i < len(a), (a[i] == a_in[i])
        assert x < len(a)  # this is actually an invariant
        #PREMISES FOR NEXT LINE: 
        # (x < len(a))
        # (x >= 0)
        # forall 0 <= i < x, (a[i] == (a_in[i] * a_in[i]))
        # forall x <= i < len(a), (a[i] == a_in[i])
        a[x] = a[x] * a[x]
        #PREMISES FOR ATTACHED PROOF, IF ANY: 
        # (a[x] == (a_old[x] * a_old[x]))
        # (x < len(a_old))
        # (x >= 0)
        # forall 0 <= i < x, (a_old[i] == (a_in[i] * a_in[i]))
        # forall x <= i < len(a_old), (a_old[i] == a_in[i])
        # (len(a) == len(a_old))
        # forall 0 <= _i < len(a), ((_i == x) or (a_old[_i] == a[_i]))
        # forall 0 <= i < x, (a[i] == (a_in[i] * a_in[i]))
        # forall (x + 1) <= i < len(a), (a[i] == a_in[i])
        """{ 1.OK  a[x] == a_old[x] * a_old[x]                        premise
             2.OK forall 0 <= i < x, a[i] == (a_in[i] * a_in[i])      premise
             3.OK forall x <= i < len(a_old), a_old[i] == a_in[i]     premise
             4.OK a_old[x] == a_in[x]                                 foralle x 3
             5.OK a[x] == a_in[x] * a_in[x]                           subst 4 1
             6.OK forall 0 <= i < (x+1), a[i] == (a_in[i] * a_in[i])  foralli 2 5
             7.OK forall (x+1) <= i < len(a), a[i] == a_in[i]         premise
             8.OK return 6 7
        }"""
        #PREMISES FOR NEXT LINE: 
        # forall 0 <= i < (x + 1), (a[i] == (a_in[i] * a_in[i]))
        # forall (x + 1) <= i < len(a), (a[i] == a_in[i])
        x = x + 1
        #PREMISES FOR ATTACHED PROOF, IF ANY: 
        # (x == (x_old + 1))
        # forall 0 <= i < (x_old + 1), (a[i] == (a_in[i] * a_in[i]))
        # forall (x_old + 1) <= i < len(a), (a[i] == a_in[i])
        """{ 1.OK forall 0 <= i < (x_old+1), a[i] == (a_in[i] * a_in[i]) premise
             2.OK forall (x_old + 1) <= i < len(a), a[i] == a_in[i]     premise
             3.OK x == x_old + 1                                       premise
             4.OK forall 0 <= i < x, a[i] == (a_in[i] * a_in[i])       subst 3 1
             5.OK forall x <= i < len(a), a[i] == a_in[i]              subst 3 2
             6.OK return 4 5
        }"""
        #PREMISES FOR NEXT LINE: 
        # forall 0 <= i < x, (a[i] == (a_in[i] * a_in[i]))
        # forall x <= i < len(a), (a[i] == a_in[i])
    #PREMISES FOR NEXT LINE: 
    # (forall 0 <= i < x, (a[i] == (a_in[i] * a_in[i])) and forall x <= i < len(a), (a[i] == a_in[i]))
    # not (x != len(a))

    """{ 1.OK (forall 0 <= i < x, a[i] == (a_in[i] * a_in[i])) and (forall x <= i < len(a), (a[i] == a_in[i]))                       premise
         2.OK not (x != len(a))                      premise
         3.OK x == len(a)                            algebra 2
         4.OK forall 0 <= i < x, a[i] == (a_in[i] * a_in[i])   ande 1
         5.OK forall 0 <= i < len(a), a[i] == (a_in[i] * a_in[i])   subst 3 4
    }"""
    #PREMISES FOR NEXT LINE: 
    # forall 0 <= i < len(a), (a[i] == (a_in[i] * a_in[i]))
#PREMISES FOR NEXT LINE: 
# (a == [])

