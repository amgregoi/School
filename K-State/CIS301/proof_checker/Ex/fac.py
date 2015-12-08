
"""{ def mult(0) == 1
     def mult(n) == mult(n-1) * n  }"""

def fac(n) :
    """{ pre  n >= 0
         post  ans == mult(n)
         return ans  }"""
    if n == 0 :
        ans = 1
        """{ 1. mult(0) == 1    def
             2. ans == mult(0)  algebra 1
             3. n == 0          premise
             4. ans == mult(n)  subst 3 2}"""
    else :
        """{ 1. not(n == 0)   premise
             2. n - 1 >= 0    algebra 1
        }"""
        sub = fac(n-1)
        """{ 1.  sub == mult(n-1)    premise }"""
        ans = n * sub
        """{ 1.  ans == n * sub             premise
             2.  sub == mult(n-1)           premise
             3.  ans == n * mult(n-1)       subst 2 1
             6.  ans == mult(n-1) * n       algebra 3
             4.  mult(n) == mult(n-1) * n   def
             5.  ans == mult(n)             subst 4 6
        }"""
    """{ 1.  ans == mult(n)                 premise  }"""
    return ans


