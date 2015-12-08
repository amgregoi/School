
x = readInt() 

if x < 0:
    """{ 1. x < 0    premise  }"""
    x = 0 - x
    """{ 1. x == 0 - x_old     premise
       2. x_old < 0            premise
       3. x > 0                algebra 1 2
    }"""
else:
    """{ 1. not(x < 0)   premise
       2. x >= 0         algebra 1
    }"""
    pass
    """{ 1. x >= 0       premise }"""

# prove here that  x >= 0 :

"""{ 1. (x > 0)  or  (x >= 0)    premise
     2. x >= 0                   ore 1
}"""
