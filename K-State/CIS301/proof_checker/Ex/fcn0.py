
a = 0
"""{ globalinv  a >= 0 }"""

def f(x) :
    """{ pre x > 0
         post ans > x  and  ans > a
         return ans  }"""
    global a
    ans = (a + x) + 1
    return ans

b = 1
c = f(b)
"""{ 1.  c > b and c > a   premise 
     3.  a >= 0            globalinv
     4.  c > 0             algebra 1 3
}"""

