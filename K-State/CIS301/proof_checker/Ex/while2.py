
i = 0
sum = 0
"""{
     1. i == 0  premise
     2. sum == 0 premise
}"""
while i != n :
    """{ invariant sum == x* i  modifies i, sum }"""
    sum = sum + x
    """{
     1. sum == sum_old + x  premise
     2.  sum_old  == x * i     premise
     3.  sum == (x*i) + x      algebra 2 1
    }"""
    i = i + 1
    """{
     1. i == i_old + 1  premise
     2. sum == (x * i_old) + x   premise
     4. sum == x * i            algebra  2
    }"""

"""{ 1. sum == x* i  premise
     2.  not ( i != n)   premise
     3.  i == n       algebra 2
     4.  sum == x * n   subst 3 1
}"""
