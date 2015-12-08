x = readInt()
y = readInt()

if x > y :
    """{ 1. x > y     premise  }"""
    max = x
    """{ 1. x > y     premise
         2. max == x  premise
         3. (x > y  and  max == x)  andi 1 2
    }"""
else :
    """{ 1. not(x > y)       premise
         2. y >= x            algebra 1
    }"""
    max = y
    """{ 1. max == y                premise
         2. y >= x                  premise
         3. y >= x  and  max == y   andi 2 1
    }"""

"""{ 1. (x > y and max == x)  or  (y >= x and max == y)   premise
     2. max >= x  and  max >= y                           ore 1  
}"""
