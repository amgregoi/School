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
    }"""
else :
    max = y
    """{ 1.  not x > y    premise
         2.  y >= x       algebra 1 
         4.  max >= y     algebra 
         5.  max >= x     algebra 
         3.  max >= x  or  (0 == 1)   ori 5
         6. max >= x  and  max >= y   andi 5 4
         7.  max >= y                 ande 6
         8.  return 6
    }"""

"""{ 1. ( max >= x  and  max >= y) or ( max >= x  and  max >= y)    premise
     2. max >= x  and  max >= y     ore 1
     3.   max >=  y                 ore 1
}"""
