
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


n = readInt()
assert n >= 0
i = 0
fac = 1
while i != n :
    print "(a) new iteration: n=", n, " i=", i, " fac=", fac
    i = i + 1
    fac = fac * i

print "(b) quit loop: n=", n, " i=", i, " fac=", fac

