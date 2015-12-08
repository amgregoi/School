
"""{ def mult(0,x) == 0
     def mult(n,x) == mult(n-1,x) + x
}"""

y = readInt() 

"""{ 1. mult(1,y) == mult(1-1,y) + y    def
     2. mult(1-1,y) == mult(0,y)       algebra
     3. mult(1,y) == mult(0,y) + y     subst 2 1
}"""
