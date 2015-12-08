# Q3.py
x = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
assert x >= 0
#PREMISES FOR NEXT LINE: 
# (x >= 0)
"""{ 1.OK x >= 0 premise	}"""
#PREMISES FOR NEXT LINE: 
# (x >= 0)
a = x + x
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (a == (x + x))
# (x >= 0)
"""{ 1.OK a == x + x premise}"""
#PREMISES FOR NEXT LINE: 
# (a == (x + x))
x = 1
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (x == 1)
# (a == (x_old + x_old))
"""{ 1.OK x == 1 premise}"""
#PREMISES FOR NEXT LINE: 
# (x == 1)
x = a + x
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (x == (a + x_old))
# (x_old == 1)
"""{ 1.OK x == a + x_old premise
	 2.OK x_old == 1 premise
	 7.OK x > 0 algebra 1
	 8.OK x > a algebra 1}"""
#PREMISES FOR NEXT LINE: 
# (x > a)
# prove:  x > a and x > 0
