x = readInt()
if x > 0 :
	"""{1. x>0	premise}"""
	y = x + 1
	"""{1. x > 0	premise
	2. y == x+1	premise
	3. y > 0	algebra 2 1
	4. y > x	algebra 2 1
	5. y> 0 and y>x andi 3 4
	}"""
else :
	"""{1. not(x>0)	premise}"""
	y = 0 - x
	"""{1. not(x>0)	premise
	2. y == 0-x	premise
	3. y + x == 0	algebra 2
	4. y >= 0	algebra 3 1
	5. y >= x 	algebra 3 1
	6. y>= 0 and y>=x andi 4 5
	}"""
# prove here that  y > 0  and  y > x