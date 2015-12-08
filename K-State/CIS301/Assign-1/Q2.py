# Q2.py
x = readInt()
y = x + 1
"""{ 1. y ==(x+1)	premise }"""
x = x - 2
"""{ 1. x == x_old - 2	premise
	 2. y == x_old + 1 	premise
	 3. x_old == y - 1	algebra 2
	 4. x == (y-1)-2	subst 3 1
	 5. x + 3 == y		algebra 4
	}"""
	 
# prove:  y == 3 + x

