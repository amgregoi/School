# Q3.py
n = readInt()
m = readInt()
a = n
b = m

while  b != 0 :
	"""{ invariant  (a - b) == (n - m)
		modifies  a, b  }"""
	a = a - 1	# insert an assignment command here
	"""{1. a == a_old -1	premise
		2. a_old-b == n-m	premise
		3. a_old == a+1	algebra 1
		4. a+1 == (n-m)+b	algebra 2 3
	}"""
	b = b - 1
	"""{1.b == b_old -1	premise
		2. b_old == b+1 algebra 1
		3. a+1 == (n-m)+ b_old	premise
		4. a+1 == (n-m)+(b+1)algebra 3 2
		5. a == (n-m) + b	algebra 4
		6. a-b == n-m	algebra 5
	}"""
"""{1. a-b == n-m	premise
	2. not(b != 0)	premise
	3. b == 0	algebra 2
	4. a == n-m	algebra 1 3
}"""
print "n - m ==", a

