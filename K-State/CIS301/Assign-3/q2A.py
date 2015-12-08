# Q2.py
n = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
assert n >= 0
#PREMISES FOR NEXT LINE: 
# (n >= 0)
x = 0
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (x == 0)
# (n >= 0)
#PREMISES FOR NEXT LINE: 
# (x == 0)
# (n >= 0)
y = 0
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (y == 0)
# (x == 0)
# (n >= 0)
"""{1.OK x == 0	premise
	2.OK y == x * n	algebra 1
}"""
#PREMISES FOR NEXT LINE: 
# (y == (x * n))


while x != n :
	"""{ invariant  y == x * n
		modifies  y, x  }"""	
	#PREMISES FOR LOOP BODY: 
	# (x != n)
	# (y == (x * n))
	y = y + n
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (y == (y_old + n))
	# (x != n)
	# (y_old == (x * n))
	"""{1.OK y == y_old + n	premise
		2.OK y_old == (x*n)	premise
		3.OK y-n == x*n	algebra 1 2
		4.OK y == (x+1) * n	algebra 3
	}"""
	#PREMISES FOR NEXT LINE: 
	# (y == ((x + 1) * n))
	x = x + 1
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (x == (x_old + 1))
	# (y == ((x_old + 1) * n))
	"""{1.OK x == x_old + 1	premise
		2.OK y == (x_old + 1) * n	premise
		3.OK y == x * n	algebra 1 2
	}"""
	#PREMISES FOR NEXT LINE: 
	# (y == (x * n))
#PREMISES FOR NEXT LINE: 
# (y == (x * n))
# not (x != n)


# PROVE HERE THAT: y == n * n
"""{1.OK not(x != n)	premise
	2.OK x == n	algebra 1
	3.OK y == x * n	premise
	4.OK y == n * n	subst 2 3
}"""
#PREMISES FOR NEXT LINE: 
# (y == (n * n))
print y
#PREMISES FOR NEXT LINE: 
# (y == (n * n))
