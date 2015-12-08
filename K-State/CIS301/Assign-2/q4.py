# Q4.py
bal = readInt()
assert bal >= 0   # bal  is a global variable that holds an account's balance
"""{1. bal >= 0	premise }"""
# function  withdraw  extracts  amt  from the balance and returns  cash
def withdraw(amt) :
    """{ pre  bal >= 0 and amt >= 0
         post bal >= 0 and bal + cash == bal_in
         return cash
    }"""
    global bal  # Python requires this line when a function changes a global var
    # bal_in = bal  (The checker adds this "ghost assignment")
    # This generates a new premise you can use:  bal == bal_in
	if amt <= bal:
		"""{1. amt <= bal	premise
			2. bal == bal_in	premise
			3. bal>= 0 and amt >= 0	premise
			4. bal >= 0	ande 3
			5. amt >= 0	ande 3
		}"""
		bal = bal - amt
		"""{1. bal == bal_old - amt		premise
			2. amt >= 0	premise
			3. amt == bal_in - bal	algebra 1
			4. bal_in - bal >= 0	algebra 2 3
			5. bal >= 0	algebra 4
		}"""
		cash = amt
		"""{1. amt == bal_in - bal	premise
			2. cash == amt	premise
			3. bal >= 0	premise
			4. cash == bal_in - bal	algebra 2 1
			5. bal+cash == bal_in	algebra 4
			6. bal >= 0	algebra 2 3
		}"""
	else :
		"""{1. not(amt <= bal)	premise
			2. bal == bal_in	premise
			3. bal>= 0 and amt >= 0	premise
			4. bal >= 0	ande 3
			5. amt >= 0	ande 3
			6. bal >= 0 and bal + cash == bal_in
		}"""
		cash = 0
		"""{1. cash == 0	premise
			3. not(amt <= bal)	premise
			4. bal == bal_in	premise
			5. bal>= 0 and amt >= 0	premise
			6. bal >= 0	ande 5
			7. amt >= 0	ande 5
			8. bal >= 0 and bal + cash == bal_in
			
		}"""
    # Prove the postcondition here; the checker can't do this one alone.
    return cash
	"""{1. bal >= 0 and bal + cash == bal_in	premise
	}"""