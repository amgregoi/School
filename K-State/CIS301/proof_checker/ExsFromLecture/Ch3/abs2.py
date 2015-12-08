
def absValue(x) :
    """{ pre  x != 0
         post ans > 0
         return ans
    }"""
    if x < 0 :
        """{ 1. x != 0    premise
             2. x < 0     premise
        }"""
        ans = 0 - x
        """{ 1. x < 0         premise
             2. ans == 0 - x  premise
             3. ans > 0       algebra 1 2
        }"""
    else :
        """{ 1. x != 0       premise
             2. not(x < 0)   premise
             3. x >= 0       algebra 2
             4. x > 0        algebra 1 3
        }"""
        ans = x
        """{ 1.  ans == x   premise
             2.  x > 0      premise
             3.  ans > 0    subst 1 2
        }"""
    """{ 1.  ans > 0         premise   }"""  
    # that is, we proved (ans > 0  or  ans > 0), which is  ans > 0
    return ans
    # we proved the postcondition



n = readInt()
if n == 0 :
    """{ 1.  n == 0    premise  }"""
    n = n + 1
    """{ 1.  n == n_old + 1      premise
         2.  n_old == 0           premise
         3.  n != 0               algebra 1 2
    }"""
else :
    """{ 1. not(n == 0)     premise
         2. n != 0         algebra 1
    }"""
    pass
    """{ 1. n != 0     premise }"""
"""{ 1.  n != 0        premise  }"""  # from the conditional
m = absValue(n)
"""{ 1.  m > 0    premise }"""  # from the function call postcondition

# prove here that  m > 0

