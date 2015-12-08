# Q1:  double returns an int that is twice as large as its int argument, n"""
def double(n) :
	"""{ pre  n >= 0
		post ans == 2 * n
		return ans
	}"""
	#PREMISES FOR NEXT LINE: 
	# (n >= 0)
	if n == 0 :
		#PREMISES FOR THEN-ARM: 
		# (n == 0)
		# (n >= 0)
		ans = 0
		#PREMISES FOR ATTACHED PROOF, IF ANY: 
		# (ans == 0)
		# (n == 0)
		# (n >= 0)
		"""{1.OK n == 0	premise
			2.OK ans == 0	premise
			3.OK ans == 2*n	algebra 1 2
		}"""
		#PREMISES FOR NEXT LINE: 
		# (ans == (2 * n))
	else :
		#PREMISES FOR ELSE-ARM: 
		# not (n == 0)
		# (n >= 0)
		subans = double(n - 1)
		#PREMISES FOR ATTACHED PROOF, IF ANY: 
		# (subans == (2 * (n - 1)))
		# not (n == 0)
		# (n >= 0)
		#PREMISES FOR NEXT LINE: 
		# (subans == (2 * (n - 1)))
		# not (n == 0)
		# (n >= 0)
		ans = subans + 2
		#PREMISES FOR ATTACHED PROOF, IF ANY: 
		# (ans == (subans + 2))
		# (subans == (2 * (n - 1)))
		# not (n == 0)
		# (n >= 0)
		"""{1.OK not(n == 0)	premise
			2.OK n >=0	premise
			3.OK n > 0	algebra 1 2
			4.OK subans == 2 *(n-1)	premise
			5.OK ans == subans + 2	premise
			6.OK subans == ans-2	algebra 5
			7.OK ans-2 == 2*(n-1)	subst 6 4
			8.OK ans == 2*n	algebra 7
		}"""
		#PREMISES FOR NEXT LINE: 
		# (ans == (2 * n))
	#PREMISES FOR NEXT LINE: 
	# (ans == (2 * n))
	# (n >= 0)
	return ans	#PREMISES FOR NEXT LINE: 
	# (ans == (2 * n))
	# (n >= 0)
#PREMISES FOR NEXT LINE: 
