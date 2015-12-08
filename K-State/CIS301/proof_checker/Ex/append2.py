
a = [4,6,8]
"""{ 1.  a == [4,6,8]   premise
     2.  a[0] == 4      algebra 1
     3.  len(a) == 3    algebra 1
}"""
i = readInt()
assert i >= 0  and i < len(a)
a[i] =  a[0]
"""{ 1. a[i] == a_old[0]   premise
     2. a[i] == 4          algebra 1
}"""
a.append(10)
"""{ 1. a[len(a)-1] == 10   premise
     2. len(a) == 4         algebra
     3. a[3] == 10          algebra 1 2
}"""
