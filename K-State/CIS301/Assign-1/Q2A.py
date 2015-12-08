# Q2.py
x = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
y = x + 1
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (y == (x + 1))
"""{ 1.OK y ==(x+1)	premise }"""
#PREMISES FOR NEXT LINE: 
# (y == (x + 1))
x = x - 2
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (x == (x_old - 2))
# (y == (x_old + 1))
"""{ 1.OK x == x_old - 2	premise
	 2.OK y == x_old + 1 	premise
	 3.OK x_old == y - 1	algebra 2
	 4.OK x == (y-1)-2	subst 3 1
	 5.OK x + 3 == y		algebra 4
	}"""
#PREMISES FOR NEXT LINE: 
# ((x + 3) == y)
	 
# prove:  y == 3 + x

