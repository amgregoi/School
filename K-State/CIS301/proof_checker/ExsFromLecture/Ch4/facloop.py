"""{ def mult(0) == 1
     def mult(n) == mult(n-1) * n  }"""

n = readInt()
i = 0
fac = 1
"""{ 1. mult(0) == 1       def
     2. fac == mult(0)     algebra 1
}"""
while i != n :
    """{ invariant  fac == mult(i)
         modifies i, fac }""" 
    """{ 1. fac == mult(i)   premise   }"""
    i = i + 1
    """{ 1. i == i_old + 1          premise
         2. fac == mult(i_old)      premise  # from the invariant
         4. fac == mult(i-1)        algebra 1 2
    }"""
    fac = fac * i
    """{ 1. fac == fac_old * i         premise
         2. fac_old == mult(i-1)       premise
         3. fac == mult(i-1) * i       subst 2 1
         4. mult(i) == mult(i-1) * i   def
         5. fac == mult(i)             subst 4 3
    }"""

"""{ 1. not(i != n)      premise
     2. i == n           algebra 1
     3. fac == mult(i)   premise
     4. fac == mult(n)   subst 2 3
}"""
