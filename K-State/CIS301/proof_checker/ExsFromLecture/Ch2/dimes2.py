
# EXAMPLE: maintain invariant property:  money == dimes * 10

assert money == dimes * 10
"""{ 1. money == dimes * 10    premise  }"""

# Say that one more dime shows up:
dimes = dimes + 1
"""{ 1. dimes == dimes_old + 1     premise
  2. money == dimes_old * 10    premise
  4. money == (dimes - 1) * 10   algebra 1 2
}"""

# The amount of money is less that what it should be; fix it:
money = money + 10
"""{ 1. money_old == (dimes - 1) * 10    premise
  2. money == money_old + 10           premise
  6. money == dimes * 10               algebra 1 2
}"""

