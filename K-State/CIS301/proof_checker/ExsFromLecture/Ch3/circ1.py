
pi = 3  # sorry --- the checker handles  ints  only  )-:
c = 0

def circ(diameter) :
    """{ pre  diameter >= 0  and  pi >= 3
         post  c == pi * diameter  
    }"""
    global c   # this designates that global c will be updated
    c = pi * diameter



"""{ 1. pi == 3   premise 
     2. c ==  0   premise
     3. pi > c    algebra 1 2
}"""
novar = circ(2)   # this is a function call that returns no answer
"""{ 1.  c == pi * 2   premise
     2.  pi > c_old    premise   # c's value was changed by  circ;
                                 # this is called a _side effect_
     # ... we can do more deductions here ...
}"""
