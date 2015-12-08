
x = readInt()
y = readInt()
if x > y :
    """{ 1.  x > y   premise }"""
    max = x
    """{ 1. max == x    premise
         2. x > y       premise
         3. max >= x    algebra
         4. max >= y    algebra 3 2
         5. max >= x  and  max >= y   andi 3 4
         6. return 2 1 5
    }"""
    # andi  means ``and introduction''
else :
    max = y
    """{ 1.  not x > y    premise
         2.  y >= x       algebra 1
         4.  max == y     premise
         5.  max >= x     algebra 2 4
         3.  max >= x or (0 == 1)   ori 5
         6.  max >= y      algebra 4
         7.  max >= x  and  max >= y   andi 5 6
         8.  return 2 4 7
    }"""
"""{ 1. max >= x  and  max >= y     premise
     2. (((x > y) and (max == x)) or ((y >= x) and (max == y))) premise
     3. max == x  or  max == y      ore 2
}"""

