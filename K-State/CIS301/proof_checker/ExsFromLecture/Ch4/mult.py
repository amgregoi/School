
def readInt(message = "Type an int: ") :
    """readInt is a helper function that reads an int from the display.
       parameter: message - a string, the input prompt; default is 'Type an int:'
       returns an int, typed by the user"""
    needInput = True
    answer = ""
    while needInput :
        text = raw_input(message)
        if text.isdigit() :
            answer = int(text)
            needInput = False
    return answer

########################


x = readInt()
y = readInt()
z = 0
count = 0

while count != x :

    print "(a) x =", x, " y =", y, " count =", count, " z =", z
    """{ invariant  ??? 
         modifies  z, count }"""

    z = z + y
    count = count + 1

print "(b) x =", x, " y =", y, " count =", count, " z =", z

