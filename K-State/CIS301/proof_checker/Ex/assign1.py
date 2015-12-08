

sum = 0
x = 0
i = 0

assert sum == x* i
sum = sum + x
"""{ 1.  sum == sum_old  + x   premise
     2.  sum_old  == x * i     premise
     3.  sum == (x*i) + x      algebra 2 1
}"""
i = i + 1
"""{ 1. i == i_old + 1      premise
     2. sum == (x * i_old) + x   premise
     3.  sum == x *(i_old + 1)   algebra 2
     4. sum == x * i     algebra 3 1
}"""
