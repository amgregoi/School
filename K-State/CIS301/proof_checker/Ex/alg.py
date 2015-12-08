
x= readInt()
y = readInt()
z  = readInt()
assert x >= 0
assert x != 0
"""{ 1.  x >= 0  premise
     2.  x != 0   premise
     3.  x > 0   algebra 2 1
     4.  x == 0  premise
     5.  z == 2  algebra
}"""
