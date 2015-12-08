
# THIS PROGRAM COMPUTES  x * y  AND PLACES THE ANSWER IN  z
x = readInt()
y = readInt()
z = 0
count = 0
"""{ 1. count == 0       premise
     2. z == count * y   algebra 1  }""" 
while count != x :
    """{ invariant  z == count * y
         modifies  z, count }"""
    """{ 1. z == count * y   premise  }"""  # holds at the start 
    z = z + y
    """{ 1. z == z_old + y       premise
         2. z_old == count * y   premise
         3. z - y == count * y   algebra 1 2
         4. z == (count + 1) * y   algebra 3 
    }"""
    count = count + 1
    """{ 1. count == count_old + 1       premise
         2. z ==  (count_old + 1) * y    premise
         3. z == count * y               subst 1 2
    }"""   # invariant reproved!

# LOOP ENDS
"""{ 1. not(count != x)    premise
     2. count == x         algebra 1
     3. z == count * y     premise
     4. z == x * y         subst 2 3
}"""


