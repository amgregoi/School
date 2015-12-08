x = readInt()
y = readInt()
if x > y :
    """{ 1.OK  x > y   premise }"""
    max = x
    """{ 1.OK max == x    premise
         2.OK x > y       premise
         3.OK max >= x    algebra
         4.OK max >= y    algebra 3 2
         5.OK max >= x  and  max >= y   andi 3 4
    }"""
else :
    max = y
    """{ 1.OK  not x > y    premise
         2.OK  y >= x       algebra 1 
         4.OK  max >= y     algebra 
         5.OK  max >= x     algebra 
         3.OK  max >= x  or  (0 == 1)   ori 5
         6.OK max >= x  and  max >= y   andi 5 4
         7.OK  max >= y                 ande 6
         8.OK  return 6
    }"""
assert (((max >= x) and (max >= y)) or ((max >= x) and (max >= y)))  # UNABLE TO VERIFY

"""{ 1.?? ( max >= x  and  max >= y) or ( max >= x  and  max >= y)    premise
     2.OK max >= x  and  max >= y     ore 1
     3.OK   max >=  y                 ore 1
}"""
