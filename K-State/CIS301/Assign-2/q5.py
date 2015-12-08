#Q5.py:   a "bank account class":
bal = 0   # no money to start, but surely we will do some deposits  (-:
"""{ globalinv bal >= 0  }"""  # all methods must maintain this property

def withdraw(amt) :
    """{ pre  amt >= 0
         post bal + cash == bal_in
         return cash
    }"""
    global bal 
	"""{1. amt >= 0	premise
		2. bal >= 0	premise
		3. bal == bal_in	premise
	}"""
	if amt <= bal:
		"""{1. amt <= bal	premise
			4. bal == bal_in	premise
		}"""
		bal = bal - amt
		"""{1. bal == bal_old - amt	premise
			2. amt <= bal_old	algebra 1
			3. amt >= 0	algebra 1
			4. bal_old >= 0	algebra 1
			5. bal_old == bal_in	premise
			6. amt == bal_in - bal	algebra 1 5
		}"""
		cash = amt
		"""{1. amt == bal_in - bal	premise
			2. cash == amt	premise
			3. cash == bal_in - bal		subst 2 1
			4. bal >= 0	algebra 1
			5. bal_in == bal + cash	algebra 3
		}"""
	else :
		"""{1. not(amt <= bal)	premise
			4. bal == bal_in	premise
		}"""
		cash = 0
		"""{1. cash == 0	premise
			2. bal == bal_in	premise
			3. not(amt <= bal)	premise
			4. bal >= 0	algebra 3
		}"""
    # prove here that  bal >= 0 and bal + cash == bal_in
    return cash

def deposit(amt) :
    """{ pre amt >= 0
         post bal_in + amt == bal
    }"""
	global bal
	bal = bal + amt
    # The checker will prove this one for you *and* confirm the invariant!

# The checker will do this one, too:
def currentBalance() :
    """{ pre True
         post ans == bal
         return ans
    }"""
	ans = bal
    return ans