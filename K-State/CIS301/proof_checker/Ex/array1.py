
a = [2,4,6]
b = a
"""{ 1. forall 0 <= j < 0, b[j] > 0    foralli
     2. b[0] > 0                      algebra
     3. forall 0 <= j < 1, b[j] > 0    foralli 1 2
     4. b[1] > 0                     algebra
     5. forall 0 <= j < 2, b[j] > 0    foralli 3 4
}"""
b[0] = 1
"""{ 1. a[0] == 2  algebra
     2. b_old[0] == 2  algebra
     3.  forall (0+1) <= j < 2, b[j] > 0 premise
     4.  b[1] > 0           foralle 1 3
}"""
b[2] = a[2]
