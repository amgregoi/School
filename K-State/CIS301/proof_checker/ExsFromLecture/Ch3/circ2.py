
### A TOY MODULE ########################################

pi = 3  # sorry --- the checker handles  ints  only  )-:
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
    # as needed, we can introduce the two  globalinvs  into the proof:
    c = pi * diameter
    """{ 1.  c == pi * diameter           premise
         2.  diameter >= 0                premise
         3.  pi == 3                      globalinv
         4.  c >= 0                       algebra 1 2 3
         5.  return 1 4                   #  returns _two_ premises to show
                                          #  that post  proved and globalinv proved
    }"""
### END #########################################


# this part would be in another component that imports (uses) the module:

"""{ 1. pi == 3   globalinv
     2. c >= 0    globalinv
}"""
novar = circ(2)
"""{ 1.  c == pi * 2   premise
     2.  c >= 0        globalinv
}"""

