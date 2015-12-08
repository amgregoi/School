#Q4.py   Plays a "Price Is Right" game: "jump s  up to  goal":
#  the program guesses some ints, in jumps (multiples),
#  without going over the  goal.   The output,  score,  is the number of jumps  made.
# The program generates the highest possible score, which is formalized by this output
# condition:   (score * jump) + gap == goal  and  (gap >= 0 and  gap < jump)
#                 where   score * jump  is the int value of the final guess
#                 and  gap  is the distance between the final int guess and the goal.
jump = readInt()
goal = readInt()
assert jump > 0
assert goal >= 0

gap = goal   # gap remembers how far away our current guess is from the goal.

# we must never go negative on the gap between the number guessed and the goal:
"""{ 1. gap == goal  premise
     globalinv  gap >= 0       # establishes the global invariant that  gap >= 0
     2. return 1               # remember the initial value of gap for now
}"""

guess = 0   # the number we have guessed so far
score = 0   # how many rounds we have guessed without going over

# How to play one round of the game:
def playRound():  
	#IMPORTANT: the invariant,  gap >= 0,  is implicit in both pre and post
	# that is, it's a premise on function entry and it must be proved on function exit
	"""{ pre  gap >= jump
		post  guess_in + gap_in == guess + gap  and  guess == guess_in + jump 
	}""" 
	global guess, gap
	#guess_in = guess (the checker automatically adds this 'ghost assignment')
	# gap_in = gap     (same here)
	guess = guess + jump
	"""{1. guess == guess_old + jump premise
		2. guess_old == guess_in	premise
		3. guess == guess_in + jump	algebra 2 1
	}"""
	print "My next guess is",  guess, "!"
	gap = gap - jump
	"""{1. guess == guess_in + jump	premise
		2. gap == gap_old - jump	premise
		3. guess_in == guess - jump	algebra 1
	}"""
    
# to win the game, we repeatedly play rounds without going over:
while gap >= jump :
	"""{ invariant  score * jump == guess  and  guess + gap == goal
		modifies  guess, gap, score, void     # see comment below about 'void'
	}"""
	void = playRound()   # the function returns no answer
	"""{1. gap_old >= jump	premise
		2. guess_old + gap_old == guess + gap and guess == guess_old + jump	premise
		3. score * jump == guess_old and guess_old + gap_old == goal	premise
		4. guess_old + gap_old == guess + gap ande 2
		5. guess == guess_old + jump ande 2
		6. guess_old == guess - jump algebra 5
		7. gap_old == (guess+gap)-guess_old	algebra 4
		
	}"""
	score = score + 1
	"""{1. score == score_old + 1	premise
	}"""
	# REPROVE THE LOOP INVARIANT HERE
"""{1. not(gap >= jump)	premise
	2. score * jump == guess  and  guess + gap == goal	premise
}"""

# PROVE HERE that the game was won with a maximum score:
"""{ 1. gap >= 0       globalinv      # a globalinv is a fact that is true "everywhere"
		# ... ADD MORE PROOF STEPS HERE AND PROVE ON THE LAST LINE THAT
		#  (score * jump) + gap == goal  and  (gap >= 0 and  gap < jump)
}"""