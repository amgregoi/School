
"""Interpreter for a mini-language with variables and loops.

   Operator trees that are interpreted are defined as

PTREE ::=  [ [], CLIST ]
           where the  []  will later be replaced by a list of declarations
CLIST ::=  [ CTREE+ ]
           where  CTREE+  means one or more CTREEs
CTREE ::=  ["=", VAR, ETREE]  |  ["print", VAR]  |  ["while", ETREE, CLIST]
ETREE ::=  NUMERAL  |  VAR  |  [OP, ETREE, ETREE]
           where  OP  is either "+" or "-"


There is one crucial data structure:

  ns is a namespace --- it holds the program's variables
  and their values.  It is a Python hash table (dictionary). 
  For example, 
     ns = {'x': 2,
           'p': [['=' 'y', ['+', 'x', '1']], ['print', 'y']],
           'y': 0}, 
  holds vars  x, p, and y,  where int x has value 2,
  proc p has the command list for  y=x+1; print y  as its value,
  and int y has value 0.
"""
ns = {}


def interpretPTREE(p):
    """pre: p  is a program represented as a  PTREE ::=  [ [], CLIST ]
       post:  ns  holds all the updates commanded by program  p
    """
    interpretCLIST(p[1])   # extract the commands and execute them


def interpretCLIST(clist):
    """pre: clist  is a list of command trees:  CLIST ::=  [ CTREE+ ]
       post:  ns  holds all the updates commanded by   clist
    """
    for command in clist :
        interpretCTREE(command)


def interpretCTREE(c) :
    """pre: c  is a command represented as a CTREE:
         CTREE ::= ["=", VAR, ETREE] | ["print", VAR] | ["while", ETREE, CLIST]
       post:  ns  holds the updates commanded by  c
    """
    operator = c[0]
    if operator == "=" :   # assignment command, ["=", VAR, ETREE]
        var = c[1]   # get left-hand side
        exprval = interpretETREE(c[2])  # evaluate the right-hand side
        ns[var] = exprval  # do the assignment

    elif operator == "print" :   # print command,  ["print", VAR]
        var = c[1]
        if var in ns :   # see if variable name is defined
            ans = ns[var]  # look up its value
            print ans
        else :
            crash("variable name undefined")

    elif operator == "while" :   # while command,  ["while", ETREE, CLIST]
        expr = c[1]
        body = c[2]
        while (interpretETREE(expr) != 0) :
            interpretCLIST(body) 

    else :   # error
        crash("invalid command")


def interpretETREE(e) :
    """pre: e  is an expression represented as an ETREE:
           ETREE ::=  NUMERAL  |  VAR  |  [OP, ETREE, ETREE]
                      where OP is either "+" or "-"
      post:  ans  holds the numerical value of  e
      returns:   ans
    """
    if isinstance(e, str) and  e.isdigit() :   # a numeral
        ans = int(e)
    elif isinstance(e, str) and len(e) > 0  and  e[0].isalpha() :  # var name
        if e in ns:   # is var name  e  assigned a value in the namespace ?
            ans = ns[e]  # look up its value
        else :
            crash("variable name not a declared int")
    else :   #  [op, e1, e2]
        op = e[0]
        ans1 = interpretETREE(e[1])
        ans2 = interpretETREE(e[2])
        if op == "+" : 
            ans = ans1 + ans2
        elif op == "-" : 
            ans = ans1 - ans2
        else :
            crash("illegal arithmetic operator")
    return ans


def crash(message) :
    """pre: message is a string
       post: message is printed and interpreter stopped
    """
    print message + "! crash! core dump:", ns
    raise Exception   # stops the interpreter


def main(program) :
    """pre:  program is a  PTREE ::=  CLIST
       post:  ns  holds all updates within  program
    """
    global ns #  ns  is global to main
    ns = {}
    interpretPTREE(program)
    print "final namespace =", ns

