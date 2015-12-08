# Q3.py
x = readInt()
assert x >= 0
"""{ 1. x >= 0 premise	}"""
a = x + x
"""{ 1. a == x + x premise}"""
x = 1
"""{ 1. x == 1 premise}"""
x = a + x
"""{ 1. x == a + x_old premise
	 2. x_old == 1 premise
	 7. x > 0 algebra 1
	 8. x > a algebra 1}"""
# prove:  x > a and x > 0
