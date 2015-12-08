
### INTERPRETER FOR OBJECT-ORIENTED LANGUAGE

"""The interpreter processes parse trees of this format:

PTREE ::=  DLIST CLIST
DLIST ::=  []
CLIST ::=  [ CTREE* ]
      where   CTREE*  means zero or more  CTREEs
CTREE ::=  ["=", LTREE, ETREE]  |  ["if", ETREE, CLIST, CLIST]
        |  ["print", ETREE]
ETREE ::=  NUM  |  [OP, ETREE, ETREE] |  ["deref", LTREE]
      where  OP ::= "+" | "-"
LTREE ::=  ID
NUM   ::=  a nonempty string of digits
ID    ::=  a nonempty string of letters


The interpreter computes the meaning of the parse tree, which is
a sequence of updates to heap storage.
"""

from heapmodule import *   # import the contents of the  heapmodule.py  module 


### INTERPRETER FUNCTIONS, one for each class of parse tree listed above.
#   See the end of program for the driver function,  interpretPTREE

def interpretDLIST(dlist) :
    """pre: dlist  is a list of declarations,  DLIST ::=  [ DTREE+ ]
       post:  memory  holds all the declarations in  dlist
    """
    for dec in dlist :
        interpretDTREE(dec)


def interpretDTREE(d) :
    """pre: d  is a declaration represented as a DTREE:
       DTREE ::= ["int", I, ETREE]
       post:  heap is updated with  d
    """
    ### WRITE ME
    if d[0] == "int" : # int declarations
        declarevar(activeNS(), d[1], interpretETREE(d[2]))
    elif d[0] == "proc" : #proc delcarations
        allocateClosure(activeNS(), d[1], d[2], d[3])	

		
def interpretCLIST(clist) :
    """pre: clist  is a list of commands,  CLIST ::=  [ CTREE+ ]
                  where  CTREE+  means  one or more CTREEs
       post:  memory  holds all the updates commanded by program  p
    """
    for command in clist :
        interpretCTREE(command)


def interpretCTREE(c) :
    """pre: c  is a command represented as a CTREE:
       CTREE ::=  ["=", LTREE, ETREE]  |  ["if", ETREE, CLIST, CLIST2] 
        |  ["print", LTREE] 
       post:  heap  holds the updates commanded by  c
    """
    operator = c[0]
    if operator == "=" :   # , ["=", LTREE, ETREE]
        handle, field = interpretLTREE(c[1])
        rval = interpretETREE(c[2])
        store(handle, field, rval)
    elif operator == "print" :   # ["print", LTREE]
        print interpretETREE(c[1])
        #printHeap()
    elif operator == "if" :   # ["if", ETREE, CLIST1, CLIST2]
        test = interpretETREE(c[1])
        if test != 0 :
            interpretCLIST(c[2])
        else :
            interpretCLIST(c[3])
    elif operator == "call" :
        handle = lookup(activeNS(), c[1])
        
        proc = lookupheap(handle)
        if isinstance(proc, list):
            p, il, cl, phandle = proc
            args = c[2]

            vals = []
            for item in args :
                vals.append(interpretETREE(item))

            newHandle = allocateNS()
            namespace = lookupheap(newHandle)
            namespace['parentns'] = phandle
            storeheap(newHandle, namespace)

            for index in range(0, len(il)):
                declarevar(newHandle, il[index], vals[index])

            interpretDLIST(il)
            interpretCLIST(cl)
            deallocateNS()
        else : crash(c, "invalid command")  
    else :  crash(c, "invalid command")


def interpretETREE(etree) :
    """interpretETREE computes the meaning of an expression operator tree.
         ETREE ::=  NUM  |  [OP, ETREE, ETREE] |  ["deref", LTREE] 
         OP ::= "+" | "-"
        post: updates the heap as needed and returns the  etree's value
    """
    if isinstance(etree, str) and etree.isdigit() :  # NUM
      ans = int(etree) 
    elif  etree[0] in ("+", "-") :      # [OP, ETREE, ETREE]
        ans1 = interpretETREE(etree[1])
        ans2 = interpretETREE(etree[2])
        if isinstance(ans1,int) and isinstance(ans2, int) :
            if etree[0] == "+" :
                ans = ans1 + ans2
            elif etree[0] == "-" :
                ans = ans1 - ans2
        else : crash(etree, "addition error --- nonint value used")
    elif  etree[0] == "deref" :    # ["deref", LTREE]
        handle, field = interpretLTREE(etree[1])
        ans = lookup(handle,field)
    else :  crash(etree, "invalid expression form")
    return ans


def interpretLTREE(ltree) :
    """interpretLTREE computes the meaning of a lefthandside operator tree.
          LTREE ::=  ID
       post: returns a pair,  (handle,varname),  the L-value of  ltree
    """
    if isinstance(ltree, str) :  #  ID ?
        ans = (activeNS(), ltree)    # use the handle to the active namespace
    else :
        crash(ltree, "illegal L-value")
    return ans


def crash(tree, message) :
    """pre: tree is a parse tree,  and  message is a string
       post: tree and message are printed and interpreter stopped
    """
    print "Error evaluating tree:", tree
    print message
    print "Crash!"
    printHeap()
    raise Exception   # stops the interpreter


### MAIN FUNCTION

def interpretPTREE(tree) :
    """interprets a complete program tree
       pre: tree is a  PTREE ::= [ DLIST, CLIST ]
       post: heap holds all updates commanded by the  tree
    """
    initializeHeap()
    interpretDLIST(tree[0])
    interpretCLIST(tree[1])
    print "Successful termination."
    printHeap()

