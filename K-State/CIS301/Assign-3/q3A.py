# Q3.py
n = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
m = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
a = n
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (a == n)
#PREMISES FOR NEXT LINE: 
# (a == n)
b = m
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (b == m)
# (a == n)
#PREMISES FOR NEXT LINE: 
# (b == m)
# (a == n)

while  b != 0 :
	"""{ invariant  (a - b) == (n - m)
		modifies  a, b  }"""
	#PREMISES FOR LOOP BODY: 
	# (b != 0)
	# ((a - b) == (n - m))
	a = a - 1	# insert an assignment command here
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (a == (a_old - 1))
	# (b != 0)
	# ((a_old - b) == (n - m))
	"""{1.OK a == a_old -1	premise
		2.OK a_old-b == n-m	premise
		3.OK a_old == a+1	algebra 1
		4.OK a+1 == (n-m)+b	algebra 2 3
	}"""
	#PREMISES FOR NEXT LINE: 
	# ((a + 1) == ((n - m) + b))
	b = b - 1
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (b == (b_old - 1))
	# ((a + 1) == ((n - m) + b_old))
	"""{1.OKb == b_old -1	premise
		2.OK b_old == b+1 algebra 1
		3.OK a+1 == (n-m)+ b_old	premise
		4.OK a+1 == (n-m)+(b+1)algebra 3 2
		5.OK a == (n-m) + b	algebra 4
		6.OK a-b == n-m	algebra 5
	}"""
	#PREMISES FOR NEXT LINE: 
	# ((a - b) == (n - m))
#PREMISES FOR NEXT LINE: 
# ((a - b) == (n - m))
# not (b != 0)
"""{1.OK a-b == n-m	premise
	2.OK not(b != 0)	premise
	3.OK b == 0	algebra 2
	4.OK a == n-m	algebra 1 3
}"""
#PREMISES FOR NEXT LINE: 
# (a == (n - m))
print "n - m ==", a
#PREMISES FOR NEXT LINE: 
# (a == (n - m))

