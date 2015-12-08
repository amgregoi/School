
g = [2,4]
"""{ globalinv  g[0] > 0 and len(g) >= 1 }"""

def f(x,y):
   """{ pre    x == 0  and y > x
        post   g[0] > x  
        return  x    
   }"""
   global g
   g[x] = y
   return  x

useless = f(0,2)
"""{ 1. (g[0] > 0) and (len(g) >= 1)   premise
     2. g[0] > 0                       globalinv
 }"""

