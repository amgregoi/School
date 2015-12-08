
def add(x,y) :
    """{ pre  x >= 0
         post  ans == x * y
         return ans
    }"""
    if x == 0 :
        ans = 0
    else :
        """{ 1. not(x == 0)  premise
             5.  x != 0      algebra 1
             2. x >= 0  premise
             3. x > 0   algebra 2 5
             4. (x -1) >= 0   algebra 3
        }"""
        sub = add(x-1, y)
        ans = sub + x
    return ans


