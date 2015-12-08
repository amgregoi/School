
x= readInt()
y = readInt()
z  = readInt()
assert x >= 0
assert x != 0
assert (x == 0)  # UNABLE TO VERIFY
assert (z == 2)  # UNABLE TO VERIFY
"""{ 1.OK  x >= 0  premise
     2.OK  x != 0   premise
     3.OK  x > 0   algebra 2 1
     4.??  x == 0  premise
     5.??  z == 2  algebra
}"""
