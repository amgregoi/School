# Q4.py
money = readInt()
withdraw = readInt()
assert money > 0 and withdraw < money
"""{ 1. money > 0 and withdraw < money premise}"""
money = money - withdraw
"""{1. money == money_old - withdraw premise
    2. money > 0 algebra 1}"""
# prove:   money > 0
