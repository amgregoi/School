
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


hours = readInt("Type an int > 2: ")

assert hours > 2
# execution reaches here _only if_ the value assigned to hours is > 2

minutes = hours * 60
# here, we _know_ that minutes > 120

print hours, minutes

raw_input()   # pauses execution till user presses Enter
