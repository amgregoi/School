
n = 999
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (n == 999)
#PREMISES FOR NEXT LINE: 
# (n == 999)
x = 999
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (x == 999)
# (n == 999)
#PREMISES FOR NEXT LINE: 
# (x == 999)
# (n == 999)
i = 0
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (i == 0)
# (x == 999)
# (n == 999)
#PREMISES FOR NEXT LINE: 
# (i == 0)
# (x == 999)
# (n == 999)
sum = 0
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (sum == 0)
# (i == 0)
# (x == 999)
# (n == 999)
"""{
     1.OK i == 0  premise
     2.OK sum == 0 premise
     3.OK  sum == x * i  algebra 2 1
     4.OK n == 999  premise
     5.OK return 3 4
}"""
#PREMISES FOR NEXT LINE: 
# (sum == (x * i))
# (n == 999)
while i != n :
    """{ invariant sum == x* i  modifies i sum }"""
    #PREMISES FOR LOOP BODY: 
    # (i != n)
    # (sum == (x * i))
    # (n == 999)
    sum = sum + x
    #PREMISES FOR ATTACHED PROOF, IF ANY: 
    # (sum == (sum_old + x))
    # (i != n)
    # (sum_old == (x * i))
    # (n == 999)
    """{
     1.OK sum == sum_old + x  premise
     2.OK  sum_old  == x * i     premise
     3.OK  sum == (x*i) + x      algebra 2 1
    }"""
    #PREMISES FOR NEXT LINE: 
    # (sum == ((x * i) + x))
    i = i + 1
    #PREMISES FOR ATTACHED PROOF, IF ANY: 
    # (i == (i_old + 1))
    # (sum == ((x * i_old) + x))
    """{
     1.OK i == i_old + 1  premise
     2.OK sum == (x * i_old) + x   premise
     3.OK sum == x * (i_old + 1)   algebra 2
     4.OK sum == x * i     subst 1 3
     5.OK sum == x * i  subst 1 3
    }"""
    #PREMISES FOR NEXT LINE: 
    # (sum == (x * i))
#PREMISES FOR NEXT LINE: 
# (sum == (x * i))
# not (i != n)
# (n == 999)

"""{ 1.OK sum == x* i  premise
     2.OK  not ( i != n)   premise
     3.OK  i == n       algebra 2
     4.OK  sum == x * n   subst 3 1
}"""
#PREMISES FOR NEXT LINE: 
# (sum == (x * n))
