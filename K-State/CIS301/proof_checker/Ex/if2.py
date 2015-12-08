x = readInt()
y = 1 
if (y == 0) and (x == 1) :
    """{ 1. (y == 0) and (x == 1)    premise }"""
    # The premise on Line 1 must be exactly as stated on the  if's test.
    p = 1
    """{ 1. p == 1      premise
         2. p == x * y  algebra 1
         3. y == 1      algebra
         4. p == x      algebra 2 3
    }"""
    # Line 2 forces the checker to consult its internal premises list.
else :
    p = x * y
    """{ 1.  not((y == 0) and (x == 1) )   premise 
         2.  (y != 0) or (x != 1)          algebra 1
         3.  p == x * y                    premise
         4.  p == x                        ore 2 3
    }"""

"""{
     2.  p == x                       premise 
     1.  (p == x) or (p == x)         algebra 2
}"""

# goal: p == x
