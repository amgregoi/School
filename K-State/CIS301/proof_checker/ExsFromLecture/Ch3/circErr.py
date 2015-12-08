
### MODULE ########################################

pi = 3  # sorry --- the checker handles  int  only  )-:
c = 0
"""{ 1.  c == 0    premise
     2.  c >= 0    algebra 1
}"""
"""{ globalinv c >= 0  
     globalinv pi == 3  }"""

def circ(diameter) :
    """{ pre  diameter >= 0 
         post  c == pi * diameter  
    }"""
    global c
    c = pi * diameter
    """{ 1.  c == pi * diameter           premise
         2.  diameter >= 0                premise
         3.  pi == 3                      globalinv
         6.  c == 3 * diameter            subst 3 1  # why does algebra fail?!
         7.  c >= 0                       algebra 2 6
    }"""

### END #########################################

"""{ 1. pi == 3   globalinv
     2. c >= 0    globalinv
     3. pi >= 3   algebra 1
}"""
novar = circ(2)
"""{ 1.  c == pi * 2   premise
     2.  c >= 0        globalinv
}"""

