
def readInt(message = "Type an int: ") :
    #readInt  reads an int typed by a user from the display.
    #  param: message - a string, the input prompt; default is 'Type an int:'
    #  returns an int, typed by the user
    while True :
        text = raw_input(message).strip()
        if text[0] == "-" :
            sign = -1
            text = text[1:]
        elif text[0] == "+" :
            sign = +1
            text = text[1:]
        else :  sign = +1
        if text.isdigit() :  return  int(text) * sign

def forall(low, high, quantified_expr):
    #forall  computes the truth value of  (FORALL i)(quantified_expr)
    # params: low, high - ints;  quant_expr - a function expression of form, 
    #                                         lambda index: boolexpr_index
    # returns : True iff  boolexpr_i  is True for all i in range(low,high)
    outcomes = [ quantified_expr(i)  for i in range(low, high) ]
    return  not(False in outcomes)

