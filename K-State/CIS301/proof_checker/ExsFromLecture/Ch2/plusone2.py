
# precondition:  x > 0 and x < 100
# postcondition: x > 1 and x < 101

x = readInt()
assert x > 0 and x < 100
x = x + 1
"""{ 1. x_old > 0  and  x_old < 100  premise
     3. x == x_old + 1               premise
     8. x > 1 and x < 101            algebra 1 3
}"""
print x

