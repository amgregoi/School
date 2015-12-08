# Q3.py
# The checker verifies automatically that  sub  satisfies its pre-post-conditions:
def sub(x, y) :
    """{ pre  x > y
         post z < 0 and z + x == y
         return z
    }"""
    #PREMISES FOR NEXT LINE: 
    # (x > y)
    z = y - x
    #PREMISES FOR ATTACHED PROOF, IF ANY: 
    # (z == (y - x))
    # (x > y)
    #PREMISES FOR NEXT LINE: 
    # (z == (y - x))
    # (x > y)
# ERROR: sorry -- you must use the specified return variable in the header
    # The checker automatically proves   z < 0 and z + x == y.
    return y
    #PREMISES FOR NEXT LINE: 
    # (z == (y - x))
    # (x > y)
    # ((z < 0) and ((z + x) == y))
#PREMISES FOR NEXT LINE: 

# Your work starts here:
a = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
assert a > 0
#PREMISES FOR NEXT LINE: 
# (a > 0)
"""{1.OK a > 0 	premise}"""
#PREMISES FOR NEXT LINE: 
# (a > 0)
b = sub(2 * a, a)
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# ((b < 0) and ((b + (2 * a)) == a))
# (a > 0)
"""{1.OK a > 0 	premise
	2.OK b < 0 and b + (2 * a) == a	premise
	3.OK a == 0-b	algebra 2
}"""
#PREMISES FOR NEXT LINE: 
# (a == (0 - b))
# Prove here that   a == 0 - b