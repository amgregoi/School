# Q4.py
bal = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
assert bal >= 0   # bal  is a global variable that holds an account's balance
#PREMISES FOR NEXT LINE: 
# (bal >= 0)
"""{1.OK bal >= 0	premise }"""
#PREMISES FOR NEXT LINE: 
# (bal >= 0)
# function  withdraw  extracts  amt  from the balance and returns  cash
def withdraw(amt) :
    """{ pre  bal >= 0 and amt >= 0
         post bal >= 0 and bal + cash == bal_in
         return cash
    }"""
    global bal  # Python requires this line when a function changes a global var
    bal_in = bal
	#PREMISES FOR NEXT LINE: 
	# ((bal >= 0) and (amt >= 0))
	# (bal == bal_in)
    # bal_in = bal  (The checker adds this "ghost assignment")
    # This generates a new premise you can use:  bal == bal_in
	if amt <= bal:
		#PREMISES FOR THEN-ARM: 
		# (amt <= bal)
		# ((bal >= 0) and (amt >= 0))
		# (bal == bal_in)
		"""{1.OK amt <= bal	premise
			2.OK bal == bal_in	premise
			3.OK bal>= 0 and amt >= 0	premise
			4.OK bal >= 0	ande 3
			5.OK amt >= 0	ande 3
		}"""
		#PREMISES FOR NEXT LINE: 
		# (amt >= 0)
		bal = bal - amt
		#PREMISES FOR ATTACHED PROOF, IF ANY: 
		# (bal == (bal_old - amt))
		# (amt >= 0)
		"""{1.OK bal == bal_old - amt		premise
			2.OK amt >= 0	premise
			3.OK amt == bal_in - bal	algebra 1
			4.OK bal_in - bal >= 0	algebra 2 3
			5.OK bal >= 0	algebra 4
		}"""
		#PREMISES FOR NEXT LINE: 
		# (bal >= 0)
		cash = amt
		#PREMISES FOR ATTACHED PROOF, IF ANY: 
		# (cash == amt)
		# (bal >= 0)
		assert (amt == (bal_in - bal))  # UNABLE TO VERIFY
		"""{1.?? amt == bal_in - bal	premise
			2.OK cash == amt	premise
			3.OK bal >= 0	premise
			4.OK cash == bal_in - bal	algebra 2 1
			5.OK bal+cash == bal_in	algebra 4
			6.OK bal >= 0	algebra 2 3
		}"""
		#PREMISES FOR NEXT LINE: 
		# (bal >= 0)
	else :
		#PREMISES FOR ELSE-ARM: 
		# not (amt <= bal)
		# ((bal >= 0) and (amt >= 0))
		# (bal == bal_in)
PARSE ERROR invalid justification or malformed assertion at token:
