x = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
if x > 0 :
	#PREMISES FOR THEN-ARM: 
	# (x > 0)
	"""{1.OK x>0	premise}"""
	#PREMISES FOR NEXT LINE: 
	# (x > 0)
	y = x + 1
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (y == (x + 1))
	# (x > 0)
	"""{1.OK x > 0	premise
	2.OK y == x+1	premise
	3.OK y > 0	algebra 2 1
	4.OK y > x	algebra 2 1
	5.OK y> 0 and y>x andi 3 4
	}"""
	#PREMISES FOR NEXT LINE: 
	# ((y > 0) and (y > x))
else :
	#PREMISES FOR ELSE-ARM: 
	# not (x > 0)
	"""{1.OK not(x>0)	premise}"""
	#PREMISES FOR NEXT LINE: 
	# not (x > 0)
	y = 0 - x
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (y == (0 - x))
	# not (x > 0)
	"""{1.OK not(x>0)	premise
	2.OK y == 0-x	premise
	3.OK y + x == 0	algebra 2
	4.OK y >= 0	algebra 3 1
	5.OK y >= x 	algebra 3 1
	6.OK y>= 0 and y>=x andi 4 5
	}"""
	#PREMISES FOR NEXT LINE: 
	# ((y >= 0) and (y >= x))
#PREMISES FOR NEXT LINE: 
# (((y > 0) and (y > x)) or ((y >= 0) and (y >= x)))
# prove here that  y > 0  and  y > x