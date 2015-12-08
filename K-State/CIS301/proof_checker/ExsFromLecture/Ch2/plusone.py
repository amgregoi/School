
# precondition:  x > 0 and x < 100
# postcondition: x > 1 and x < 101

x = readInt()
assert x > 0 and x < 100
x = x + 1
"""{ 1. x_old > 0  and  x_old < 100  premise
     2. x_old > 0                    ande 1
     3. x == x_old + 1               premise
     4. x_old + 1 > 1                algebra 1
     5. x > 1                        subst 3 4
     6. x_old < 100                  ande 1
     7. x < 101                      algebra 3 6
     8. x > 1 and x < 101            andi 5 7
}"""
print x

