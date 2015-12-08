
a = 0
"""{ globalinvOK  a >= 0 }"""

def f(x) :
    """{ pre x > 0
         post ans > 0 
         return ans  }"""
    global a
    ans = (a + x) + 1
    return ans

b = f(1)
print "b =", b

