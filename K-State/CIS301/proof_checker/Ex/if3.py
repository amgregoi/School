x = readInt()
y = readInt()
if x > y :
    max = x
else :
    max = y

"""{
     1. (((max == x) and (x > y)) or ((max == y) and not (x > y)))  premise
     2. (max == x) or (max == y)         ore 1
}"""
