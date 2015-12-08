# EvalProp.py
"""Evaluator for propositional-logic operator trees (parse trees). 
   Input:  The trees are represented as nested lists and conform to this format:

    PTREE ::=  PRIM  |  ["~", PTREE]  |  ["^", PTREE1, PTREE2]  | ["v", PTREE1, PTREE2 ]
    PRIM is either  "T" or "F" or a single lower-case letter (but never "v")

    Example:   ["~", ["^", "p", "T"]]    is the tree for  ~(p ^ T)

    Output: The output is the meaning of the tree.  In each of Questions 1,2,3,4, the output changes:
    Question 1: the output is the True-False meaning of the tree, where the variables in the tree
    have  None  as value
    Question 2: the output is the True-False meaning of the tree where the variables get
    True-False values supplied by a human user
    Question 3: the output is a list of all possible True-False combinations of values to the
    variables and the accompanying meanings (a "truth table")
    Question 4: the output is the "truth table" plus statements whether or not the tree is
    a tautology or is satifiable.
"""

def eval(bindings, t) :
    """eval  computes the True-False meaning of tree  t,  using the dictionary,  bindings,
             to find the values of all VARs used in  t
       pre:   bindings  is a dictionary holding the VARs used in  t and their True-False values.  
              Example binding:   {"p"= True, "q"= False}.
              t  is an operator tree in the format define above
       post:  ans is the True/False meaning of  t         
       returns: ans
           Example:  eval({"p"= True, "q"= False}, ["~", ["^", "p", "q"]])  returns  True
    """
    if isinstance(t, str) : # is  t  a PRIM ?
        if t == "T" :
            ans = True
        elif t == "F" :
            ans = False
        elif len(t) == 1 and t.islower():  # is  t  a VAR, a single lower-case letter ?
            #ans = None   # COMMENT OUT THIS LINE FOR QUESTIONS 2-4
            # UNCOMMENT THE FOLLOWING LINE FOR QUESTIONS 2-4:
            ans = bindings[t]  # look up value of VAR       
    else :  # t is a list, which means it's a logical expression with an op:
        op = t[0]
        if op == "~" :  # ["~", PTREE]
            ans1 = eval(bindings, t[1])
            ans = not(ans1)
        elif op == "^" :  # ["^", PTREE1, PTREE2]
            ans1 = eval(bindings, t[1])
            ans2 = eval(bindings, t[2])
            ans = ans1 and  ans2
        elif op == "v" :  # ["v", PTREE1, PTREE2]
            ans1 = eval(bindings, t[1])
            ans2 = eval(bindings, t[2])
            ans = ans1 or  ans2
        else :
            error("unknown operator", op)
    return ans


def evalWithoutVars(t):
    """This function is called to supply the output for Question 1.
       pre:  t is an operator tree in the format given above
       post: computes and prints the meaning of  t  where the vars within  t  have  
             None  as their value
    """
    ans = eval({}, t)   # we do not have any bindings for vars in  t, use  {}  as the first arg
    print "The proposition's meaning with no values for its vars is:", ans


def evalVarList(t) : 
    """traverses  t  and builds a list of all the VARs embedded in  t
       pre: t  is a PTREE
       post: computes the "meaning" of  t  as  ans,  a list that holds all the VARs in  t.  
          The order of the vars does not matter, but no varname is repeated --- no duplicates!
       returns: ans
           Examples:  
           evalVarList(["v", "T", "p"])  returns  ["p"]
           evalVarList("T")  returns  []
           evalVarList(["^", ["~", "p"], ["v", "q", "p"]])  returns  ["p", "q"]
    """
    ans = {}
    test = 0
    while test != len(t): 
        if len(t[test]) == 1 :
            #print "char length: ", len(t[test])
            if t[test] != "F" and t[test] != "T" and t[test] != "~" and t[test] != "^" and t[test] != "v" :
                ans[t[test]] = t[test]
        elif len(t[test]) == 2:
            #print "char length: ", len(t[test])
            if t[test][1] != 'F' and t[test][1] != "T" and t[test][1] != "~" and t[test][1] != "^" and t[test][1] != "v" :
                ans[t[test][1]] = t[test][1]
        elif len(t[test]) == 3 :
            #print "char length: ", len(t[test])
            if t[test][1] != "F" and t[test][1] != "T" and t[test][1] != "~" and t[test][1] != "^" and t[test][1] != "v" and len(t[test][1]) == 2 :
                ans[t[test][1][1]] = evalVarList(t[test][1])
                ans[t[test][2]] = evalVarList(t[test][2])	
            elif t[test][1] != "F" and t[test][1] != "T" and t[test][1] != "~" and t[test][1] != "^" and t[test][1] != "v" and len(t[test][2]) == 2 :
                ans[t[test][1]] = evalVarList(t[test][1])
                ans[t[test][2][1]] = evalVarList(t[test][2])	
            elif t[test][1] != "F" and t[test][1] != "T" and t[test][1] != "~" and t[test][1] != "^" and t[test][1] != "v" :
                ans[t[test][1]] = evalVarList(t[test][1])
                ans[t[test][2]] = evalVarList(t[test][2])
        test = test+1
    return ans
	

		
    #return test
    #return []  # REMOVE THIS LINE AND WRITE ME TO ANSWER QUESTION 2


def evalOneTest(tree):
    """This function is called to supply the output for Question 2.
       pre:  tree  is an operator tree in the format given above
       post: computes and prints the meaning of  tree  where the vars are given 
             True-False values supplied by the user
    """
    varnames = evalVarList(tree)   # collect the vars inside tree
    print "\nVariables in proposition are", varnames
    bindings = {}   # dictionary that will hold the  var=value  pairs                        
    for name in varnames :                       
        inputval = raw_input("Type  True  or  False  for variable " + name + ": ")
        if inputval == "True" : 
            bindings[name] = True
        elif inputval == "False" :
            bindings[name] = False
        else :
            print "invalid input; binding not made"
            bindings[name] = None           
    ans = eval(bindings, tree)
    print "For bindings:", bindings,
    print " The answer is:", ans


def generateBoolPermutations(howmany):
    """generates all possible True/False permutations for  howmany  different vars
       and saves all of them in a list
       pre: howmany >= 0
       post:  ans  holds a list of all the permutations
       returns: ans
         For example, 
         generateBoolPermutations(0) = [[]]
         generateBoolPermutations(1) = [[True], [False]]  
         generateBoolPermutations(2) = [[True, True], [True,False], [False,True], [False,False]]
    """
    assert howmany >= 0
    if howmany == 0 :
        ans = [[]]
    else :
        subans = generateBoolPermutations(howmany - 1)
        ans = []
        for permutation in subans :
            ans = ans + [ permutation + [True], permutation + [False] ]
    return ans


    
def evalAllTests(tree):
    """This function is called to supply the output for Questions 3 and 4.
        It computes all possible combinations of True-False values for the variables in  tree  
        and evaluates  tree  with each combination, printing the results. 
        For Question 4: In addition, the function states whether or not  tree  is 
        a tautology (true for all True-False combinations) and whether or not  tree  is 
        satisfiable (true for at least one combination)
       pre:  tree  is an operator tree in the format given above
       post: (see the actions stated above)
    """

    varlist = evalVarList(tree)
    bindings = varlist.copy()
    temp = 0
    allcombinations = generateBoolPermutations(len(varlist))
    # INSERT HERE THE CODE TO ANSWER QUESTIONS 3 AND 4
    #print "combo", allcombinations[0]
    for num in range(0, pow(2,len(varlist))):
            count = 0
            for name in varlist :
                bindings[name] = allcombinations[num][count]
                if(len(varlist) == 1):
                    answ = eval(bindings, tree)
                    print " \n For Bindings: ", bindings, "  The Answer is: ", answ
                    if answ == True:
                        temp = temp + 1
                if (count%(len(varlist))-1) == 0 :
                    answ = eval(bindings, tree)
                    print " \n For Bindings: ", bindings, "  The Answer is: ", answ
                    if answ == True:
                        temp = temp + 1
                count = count + 1
    
    if temp == pow(2,len(varlist)) or (len(varlist) == 1 and temp == 2) :
        print "is a tautology\nis satisfiable"
    elif temp > 0 :
        print "is not a tautology\nis Satisfiable"
    elif temp == 0 :
        print"is not a tautology\nis not satisfiable"
				
				
    


def error(text, tree):
    """prints an error message and halts the evaluation"""
    print "evaluation error: " + text
    print tree
    raise Exception

