#Q5.py:   a "bank account class":
bal = 0   # no money to start, but surely we will do some deposits  (-:
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (bal == 0)
"""{ globalinvOK bal >= 0  }"""  # all methods must maintain this property
#PREMISES FOR NEXT LINE: 
# (bal >= 0)

def withdraw(amt) :
    """{ pre  amt >= 0
         post bal + cash == bal_in
         return cash
    }"""
    global bal 
    bal_in = bal
	#PREMISES FOR NEXT LINE: 
	# (amt >= 0)
	# (bal >= 0)
	# (bal == bal_in)
	"""{1.OK amt >= 0	premise
		2.OK bal >= 0	premise
		3.OK bal == bal_in	premise
	}"""
	#PREMISES FOR NEXT LINE: 
	# (bal == bal_in)
	if amt <= bal:
		#PREMISES FOR THEN-ARM: 
		# (amt <= bal)
		# (bal == bal_in)
		"""{1.OK amt <= bal	premise
			4.OK bal == bal_in	premise
		}"""
		#PREMISES FOR NEXT LINE: 
		# (bal == bal_in)
		bal = bal - amt
		#PREMISES FOR ATTACHED PROOF, IF ANY: 
		# (bal == (bal_old - amt))
		# (bal_old == bal_in)
		"""{1.OK bal == bal_old - amt	premise
			2.OK amt <= bal_old	algebra 1
			3.OK amt >= 0	algebra 1
			4.OK bal_old >= 0	algebra 1
			5.OK bal_old == bal_in	premise
			6.OK amt == bal_in - bal	algebra 1 5
		}"""
		#PREMISES FOR NEXT LINE: 
		# (amt == (bal_in - bal))
		cash = amt
		#PREMISES FOR ATTACHED PROOF, IF ANY: 
		# (cash == amt)
		# (amt == (bal_in - bal))
		"""{1.OK amt == bal_in - bal	premise
			2.OK cash == amt	premise
			3.OK cash == bal_in - bal		subst 2 1
			4.OK bal >= 0	algebra 1
			5.OK bal_in == bal + cash	algebra 3
		}"""
		#PREMISES FOR NEXT LINE: 
		# (bal_in == (bal + cash))
	else :
		#PREMISES FOR ELSE-ARM: 
		# not (amt <= bal)
		# (bal == bal_in)
		"""{1.OK not(amt <= bal)	premise
			4.OK bal == bal_in	premise
		}"""
		#PREMISES FOR NEXT LINE: 
		# (bal == bal_in)
		cash = 0
		#PREMISES FOR ATTACHED PROOF, IF ANY: 
		# (cash == 0)
		# (bal == bal_in)
		assert not (amt <= bal)  # UNABLE TO VERIFY
		"""{1.OK cash == 0	premise
			2.OK bal == bal_in	premise
			3.?? not(amt <= bal)	premise
			4.OK bal >= 0	algebra 3
		}"""
		#PREMISES FOR NEXT LINE: 
		# (bal >= 0)
# ERROR: uneven indentation of commands
    # prove here that  bal >= 0 and bal + cash == bal_in
    return cash
    #PREMISES FOR NEXT LINE: 
    # (bal >= 0)
    # ((bal + cash) == bal_in)
	#PREMISES FOR NEXT LINE: 
	# ((bal_in == (bal + cash)) or ((bal >= 0) and ((bal + cash) == bal_in)))
	assert (bal >= 0)  # UNABLE TO VERIFY
#PREMISES FOR NEXT LINE: 
# (bal >= 0)

def deposit(amt) :
    """{ pre amt >= 0
         post bal_in + amt == bal
    }"""
	global bal
	bal_in = bal
	#PREMISES FOR NEXT LINE: 
	# (amt >= 0)
	# (bal >= 0)
	# (bal == bal_in)
	bal = bal + amt
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (bal == (bal_old + amt))
	# (amt >= 0)
	# (bal_old >= 0)
	# (bal_old == bal_in)
	#PREMISES FOR NEXT LINE: 
	# (amt >= 0)
#PREMISES FOR NEXT LINE: 
# (bal >= 0)
    # The checker will prove this one for you *and* confirm the invariant!

# The checker will do this one, too:
def currentBalance() :
    """{ pre True
         post ans == bal
         return ans
    }"""
	#PREMISES FOR NEXT LINE: 
	# True
	ans = bal
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (ans == bal)
	# True
	#PREMISES FOR NEXT LINE: 
	# (ans == bal)
# ERROR: uneven indentation of commands
    return ans    #PREMISES FOR NEXT LINE: 
    # (ans == bal)
#PREMISES FOR NEXT LINE: 
# (bal >= 0)
