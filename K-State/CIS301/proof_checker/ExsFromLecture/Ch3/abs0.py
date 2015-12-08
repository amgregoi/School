
def absValue(x) :
    """{ pre  x != 0
         post ans > 0
         return ans
    }"""
    if x < 0 :
        ans = 0 - x
    else :
        ans = x
    return ans

