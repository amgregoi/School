# Q1:  double returns an int that is twice as large as its int argument, n"""
def double(n) :
	"""{ pre  n >= 0
		post ans == 2 * n
		return ans
	}"""
	if n == 0 :
		ans = 0
		"""{1. n == 0	premise
			2. ans == 0	premise
			3. ans == 2*n	algebra 1 2
		}"""
	else :
		subans = double(n - 1)
		ans = subans + 2
		"""{1. not(n == 0)	premise
			2. n >=0	premise
			3. n > 0	algebra 1 2
			4. subans == 2 *(n-1)	premise
			5. ans == subans + 2	premise
			6. subans == ans-2	algebra 5
			7. ans-2 == 2*(n-1)	subst 6 4
			8. ans == 2*n	algebra 7
		}"""
	return ans