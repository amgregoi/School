#Q4.py   Plays a "Price Is Right" game: "jump s  up to  goal":
#  the program guesses some ints, in jumps (multiples),
#  without going over the  goal.   The output,  score,  is the number of jumps  made.
# The program generates the highest possible score, which is formalized by this output
# condition:   (score * jump) + gap == goal  and  (gap >= 0 and  gap < jump)
#                 where   score * jump  is the int value of the final guess
#                 and  gap  is the distance between the final int guess and the goal.
jump = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
goal = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
assert jump > 0
#PREMISES FOR NEXT LINE: 
# (jump > 0)
assert goal >= 0
#PREMISES FOR NEXT LINE: 
# (goal >= 0)
# (jump > 0)

gap = goal   # gap remembers how far away our current guess is from the goal.
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (gap == goal)
# (goal >= 0)
# (jump > 0)

# we must never go negative on the gap between the number guessed and the goal:
"""{ 1.OK gap == goal  premise
     globalinvOK  gap >= 0       # establishes the global invariant that  gap >= 0
     2.OK return 1               # remember the initial value of gap for now
}"""
#PREMISES FOR NEXT LINE: 
# (gap == goal)

guess = 0   # the number we have guessed so far
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (guess == 0)
# (gap == goal)
#PREMISES FOR NEXT LINE: 
# (guess == 0)
# (gap == goal)
score = 0   # how many rounds we have guessed without going over
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (score == 0)
# (guess == 0)
# (gap == goal)
#PREMISES FOR NEXT LINE: 
# (score == 0)
# (guess == 0)
# (gap == goal)

# How to play one round of the game:
def playRound():  
	#IMPORTANT: the invariant,  gap >= 0,  is implicit in both pre and post
	# that is, it's a premise on function entry and it must be proved on function exit
	"""{ pre  gap >= jump
		post  guess_in + gap_in == guess + gap  and  guess == guess_in + jump 
	}""" 
	global guess, gap
	gap_in = gap
	guess_in = guess
	#PREMISES FOR NEXT LINE: 
	# (gap >= jump)
	# (gap >= 0)
	# (guess == guess_in)
	# (gap == gap_in)
	#guess_in = guess (the checker automatically adds this 'ghost assignment')
	# gap_in = gap     (same here)
	guess = guess + jump
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (guess == (guess_old + jump))
	# (gap >= jump)
	# (gap >= 0)
	# (guess_old == guess_in)
	# (gap == gap_in)
	"""{1.OK guess == guess_old + jump premise
		2.OK guess_old == guess_in	premise
		3.OK guess == guess_in + jump	algebra 2 1
	}"""
	#PREMISES FOR NEXT LINE: 
	# (guess == (guess_in + jump))
	print "My next guess is",  guess, "!"
	#PREMISES FOR NEXT LINE: 
	# (guess == (guess_in + jump))
	gap = gap - jump
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (gap == (gap_old - jump))
	# (guess == (guess_in + jump))
	"""{1.OK guess == guess_in + jump	premise
		2.OK gap == gap_old - jump	premise
		3.OK guess_in == guess - jump	algebra 1
	}"""
	#PREMISES FOR NEXT LINE: 
	# (guess_in == (guess - jump))
#PREMISES FOR NEXT LINE: 
# (score == 0)
# (guess == 0)
# (gap == goal)
    
# to win the game, we repeatedly play rounds without going over:
while gap >= jump :
	"""{ invariant  score * jump == guess  and  guess + gap == goal
		modifies  guess, gap, score, void     # see comment below about 'void'
	}"""
	#PREMISES FOR LOOP BODY: 
	# (gap >= jump)
	# (((score * jump) == guess) and ((guess + gap) == goal))
	void = playRound()   # the function returns no answer
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (((guess_old + gap_old) == (guess + gap)) and (guess == (guess_old + jump)))
	# (gap_old >= jump)
	# (((score * jump) == guess_old) and ((guess_old + gap_old) == goal))
	"""{1.OK gap_old >= jump	premise
		2.OK guess_old + gap_old == guess + gap and guess == guess_old + jump	premise
		3.OK score * jump == guess_old and guess_old + gap_old == goal	premise
		4.OK guess_old + gap_old == guess + gap ande 2
		5.OK guess == guess_old + jump ande 2
		6.OK guess_old == guess - jump algebra 5
		7.OK gap_old == (guess+gap)-guess_old	algebra 4
		
	}"""
	#PREMISES FOR NEXT LINE: 
	score = score + 1
	#PREMISES FOR ATTACHED PROOF, IF ANY: 
	# (score == (score_old + 1))
	"""{1.OK score == score_old + 1	premise
	}"""
	#PREMISES FOR NEXT LINE: 
	assert (((score * jump) == guess) and ((guess + gap) == goal))  # UNABLE TO VERIFY
#PREMISES FOR NEXT LINE: 
# (((score * jump) == guess) and ((guess + gap) == goal))
# not (gap >= jump)
	# REPROVE THE LOOP INVARIANT HERE
"""{1.OK not(gap >= jump)	premise
	2.OK score * jump == guess  and  guess + gap == goal	premise
}"""
#PREMISES FOR NEXT LINE: 
# (((score * jump) == guess) and ((guess + gap) == goal))

# PROVE HERE that the game was won with a maximum score:
"""{ 1.OK gap >= 0       globalinv      # a globalinv is a fact that is true "everywhere"
		# ... ADD MORE PROOF STEPS HERE AND PROVE ON THE LAST LINE THAT
		#  (score * jump) + gap == goal  and  (gap >= 0 and  gap < jump)
}"""#PREMISES FOR NEXT LINE: 
# (gap >= 0)
