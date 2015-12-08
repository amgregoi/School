# Q2.py
n = readInt()
assert n >= 0
x = 0
y = 0
"""{1. x == 0	premise
	2. y == x * n	algebra 1
}"""


while x != n :
	"""{ invariant  y == x * n
		modifies  y, x  }"""	
	y = y + n
	"""{1. y == y_old + n	premise
		2. y_old == (x*n)	premise
		3. y-n == x*n	algebra 1 2
		4. y == (x+1) * n	algebra 3
	}"""
	x = x + 1
	"""{1. x == x_old + 1	premise
		2. y == (x_old + 1) * n	premise
		3. y == x * n	algebra 1 2
	}"""


# PROVE HERE THAT: y == n * n
"""{1. not(x != n)	premise
	2. x == n	algebra 1
	3. y == x * n	premise
	4. y == n * n	subst 2 3
}"""
print y
