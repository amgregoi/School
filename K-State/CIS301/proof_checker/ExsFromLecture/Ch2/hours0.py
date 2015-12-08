######################################################################
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
######################################################################


hours = readInt()
assert hours > 2

minutes = hours * 60

print hours, minutes
raw_input()
