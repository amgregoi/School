# Q3.py
# The checker verifies automatically that  sub  satisfies its pre-post-conditions:
def sub(x, y) :
    """{ pre  x > y
         post z < 0 and z + x == y
         return z
    }"""
    z = y - x
    # The checker automatically proves   z < 0 and z + x == y.
    return y

# Your work starts here:
a = readInt()
assert a > 0
"""{1. a > 0 	premise}"""
b = sub(2 * a, a)
"""{1. a > 0 	premise
	2. b < 0 and b + (2 * a) == a	premise
	3. a == 0-b	algebra 2
}"""
# Prove here that   a == 0 - b