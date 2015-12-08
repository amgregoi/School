x = readInt()
y = readInt()

if x > y :
    """{ 1. x > y     premise  }"""
    max = x
    """{ 1. x > y     premise
         2. max == x  premise
         3. max >= x  algebra 2
         4. max >= y  algebra 1 3
         5. max >= x  and  max >= y   andi 3 4
    }"""
else :
    """{ 1. not (x > y)       premise
         2. y >= x            algebra 1
    }"""
    max = y
    """{ 1. max == y    premise
         2. y >= x      premise
         3. max >= y    algebra 1
         4. max >= x    algebra 1 2
         5. max >= x  and  max >= y   andi 4 3
    }"""

"""{ 1. max >= x  and  max >= y   premise  }"""
