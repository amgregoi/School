
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



m = readInt()
assert m <= 0
n = m - 1

"""{ 1. m <= 0                                premise
     2. n == m - 1                           premise
     3. m <= 0 and n == m - 1                 andi 1 2
     4. n-1 != 0                             algebra 1 2
     5. n-1 != 0 and (m <= 0 and n == m - 1)  andi 4 3
}"""
m = absValue(n-1)
"""{ 1. m > 0                                         premise  
     2. n-1 != 0 and (m_old <= 0 and n == m_old - 1)  premise
     3. m_old <= 0 and n == m_old - 1                 ande 2
     4. n - 1 <= 0                                       algebra 3
     5. m > 0  and  n - 1 <= 0                           andi 1 4
}"""

