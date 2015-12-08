# Q1.py
x = readInt()
y = readInt()
if y > x :
	ans = y - x
	"""{1.OK y > x	premise	
		2.OK ans == y-x	premise
		3.OK ans > 0 algebra 2 1
	}"""
else :
	"""{1.OK not(y>x)	premise}"""
	ans = x - y
	"""{1.OK not(y>x)	premise	
		2.OK ans == x-y	premise
		3.OK ans >= 0	algebra 2 1
	}"""
# prove  ans >= 0