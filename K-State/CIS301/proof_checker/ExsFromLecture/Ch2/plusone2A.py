
# precondition:  x > 0 and x < 100
# postcondition: x > 1 and x < 101

x = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
assert x > 0 and x < 100
#PREMISES FOR NEXT LINE: 
# ((x > 0) and (x < 100))
x = x + 1
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (x == (x_old + 1))
# ((x_old > 0) and (x_old < 100))
"""{ 1.OK x_old > 0  and  x_old < 100  premise
     3.OK x == x_old + 1               premise
     8.OK x > 1 and x < 101            algebra 1 3
}"""
#PREMISES FOR NEXT LINE: 
# ((x > 1) and (x < 101))
print x
#PREMISES FOR NEXT LINE: 
# ((x > 1) and (x < 101))

