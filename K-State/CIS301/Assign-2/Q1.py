# Q1.py
x = readInt()
y = readInt()
if y > x :
	ans = y - x
	"""{1. y > x	premise	
		2. ans == y-x	premise
		3. ans > 0 algebra 2 1
	}"""
else :
	"""{1. not(y>x)	premise}"""
	ans = x - y
	"""{1. not(y>x)	premise	
		2. ans == x-y	premise
		3. ans >= 0	algebra 2 1
	}"""
# prove  ans >= 0