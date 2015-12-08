
g = [0,0]
"""{ globalinv g[0] == 0 }"""
def f() :
    """{ pre True  post ans == 0  return ans }"""
    global g
    ans = g[0] 
    return ans

x = f()
"""{ 1. x == 0   premise }"""
