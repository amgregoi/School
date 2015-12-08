
a = [5]
"""{ 1. len(a) == 1  algebra }"""
x = readInt()
assert x > 5
a.append(x)
"""{ 1. len(a_old) == 1  premise
     2. len(a) == 2   algebra 1
}"""
pass
