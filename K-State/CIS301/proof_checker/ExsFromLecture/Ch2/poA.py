
x = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
assert x > 0
#PREMISES FOR NEXT LINE: 
# (x > 0)
x = x + 1
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (x == (x_old + 1))
# (x_old > 0)
"""{ 1.OK x == x_old + 1  premise
     2.OK x_old > 0  premise
     3.OK x > 1      algebra 1 2
}"""
#PREMISES FOR NEXT LINE: 
# (x > 1)
print x
#PREMISES FOR NEXT LINE: 
# (x > 1)

