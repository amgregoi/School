
# THIS PROGRAM COMPUTES  x * y  AND PLACES THE ANSWER IN  z
x = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
y = readInt()
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# True
#PREMISES FOR NEXT LINE: 
z = 0
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (z == 0)
#PREMISES FOR NEXT LINE: 
# (z == 0)
count = 0
#PREMISES FOR ATTACHED PROOF, IF ANY: 
# (count == 0)
# (z == 0)
"""{ 1.OK count == 0       premise
     2.OK z == count * y   algebra 1  }""" 
#PREMISES FOR NEXT LINE: 
# (z == (count * y))
while count != x :
    """{ invariant  z == count * y
         modifies  z, count }"""
    #PREMISES FOR LOOP BODY: 
    # (count != x)
    # (z == (count * y))
    """{ 1.OK z == count * y   premise  }"""  # holds at the start 
    #PREMISES FOR NEXT LINE: 
    # (z == (count * y))
    z = z + y
    #PREMISES FOR ATTACHED PROOF, IF ANY: 
    # (z == (z_old + y))
    # (z_old == (count * y))
    """{ 1.OK z == z_old + y       premise
         2.OK z_old == count * y   premise
         3.OK z - y == count * y   algebra 1 2
         4.OK z == (count + 1) * y   algebra 3 
    }"""
    #PREMISES FOR NEXT LINE: 
    # (z == ((count + 1) * y))
    count = count + 1
    #PREMISES FOR ATTACHED PROOF, IF ANY: 
    # (count == (count_old + 1))
    # (z == ((count_old + 1) * y))
    """{ 1.OK count == count_old + 1       premise
         2.OK z ==  (count_old + 1) * y    premise
         3.OK z == count * y               subst 1 2
    }"""   # invariant reproved!
    #PREMISES FOR NEXT LINE: 
    # (z == (count * y))
#PREMISES FOR NEXT LINE: 
# (z == (count * y))
# not (count != x)

# LOOP ENDS
"""{ 1.OK not(count != x)    premise
     2.OK count == x         algebra 1
     3.OK z == count * y     premise
     4.OK z == x * y         subst 2 3
}"""
#PREMISES FOR NEXT LINE: 
# (z == (x * y))


