# Q4.py
money = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
withdraw = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
assert money > 0 and withdraw < money
#PREMISES FOR NEXT LINE: 
# ((money > 0) and (withdraw < money))
"""{ 1.OK money > 0 and withdraw < money premise}"""
#PREMISES FOR NEXT LINE: 
# ((money > 0) and (withdraw < money))
money = money - withdraw
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (money == (money_old - withdraw))
# ((money_old > 0) and (withdraw < money_old))
"""{1.OK money == money_old - withdraw premise
    2.OK money > 0 algebra 1}"""
#PREMISES FOR NEXT LINE: 
# (money > 0)
# prove:   money > 0
