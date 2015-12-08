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


def interpretDTREE(d) : # covers int, proc, ob, & class declarations
    """pre: d  is a declaration represented as a DTREE:
       DTREE ::= ["int", I, ETREE]
       post:  heap is updated with  d
    """
	### WRITE ME
    if d[0] == "int" : # int declaration
        e = interpretETREE(d[2])
        if type(e) == int :
            declare(activeNS(), d[1], e)
        else :
            crash(e, "attempted to assign a non int val to an int")
    elif d[0] == "proc" : #proc allocation
        #if d[1] == "int":   
            #declare(activeNS(), d[1], e)
        allocateClosure(activeNS(), 'proc', d[1], d[2], d[3])
    elif d[0] == "ob" : # object allocation
        e = interpretETREE(d[2])
        if type(e) != int :
            declare(activeNS(), d[1], e)
        else :
            crash(e, "attempted to assign int value to ob")
    elif d[0] == "class" : #class allocation
        allocateClosure(activeNS(), 'class', d[1], [], d[2])
    else :
        crash(d[0], "not a valid delcaration!")

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
    # print c
    operator = c[0]
    if operator == "=" :   # "=" operator
        handle, field = interpretLTREE(c[1])
        rval = interpretETREE(c[2])
        store(handle, field, rval)
    elif operator == "print" :   # print operator
        print interpretETREE(c[1])
    elif operator == "if" :   # if operator
        test = interpretETREE(c[1])
        if test != 0 :
            interpretCLIST(c[2])
        else :
            interpretCLIST(c[3])
    elif operator == "call": # call operator
        tempHandle, temp = interpretLTREE(c[1])
        handle = lookup(tempHandle, temp)
        proc = lookupheap(handle)
        if isinstance(proc, list):
            p, il, cl, phandle = proc
            args = c[2]

            vals = []
            for item in args :
                vals.append(interpretETREE(item))

            newnshandle = allocateNS()
            namespace = lookupheap(newnshandle)
            namespace['parentns'] = phandle
            storeheap(newnshandle, namespace)

            for index in range(0, len(il)):
               declare(newnshandle, il[index], vals[index])

            #interpretDLIST(il)
            interpretCLIST(cl)
            deallocateNS()
        else:
            crash(c[1], "not a procedure")
    else :  crash(c, "invalid command")


def interpretETREE(etree) :
    """interpretETREE computes the meaning of an expression operator tree.
         ETREE ::=  NUM  |  [OP, ETREE, ETREE] |  ["deref", LTREE] 
         OP ::= "+" | "-"
        post: updates the heap as needed and returns the  etree's value
    """
    if isinstance(etree, str) and etree.isdigit() : #is num
        ans = int(etree)
    elif isinstance(etree, str) and etree == "nil": #is nil
        ans = "nil"
    elif  etree[0] in ("+", "-") :      #"+,-" operators
        ans1 = interpretETREE(etree[1])
        ans2 = interpretETREE(etree[2])
        if isinstance(ans1,int) and isinstance(ans2, int) :
            if etree[0] == "+" :
                ans = ans1 + ans2
            elif etree[0] == "-" :
                ans = ans1 - ans2
        else : crash(etree, "a value isn't an int")
    elif  etree[0] == "deref" :    # deref
        handle, field = interpretLTREE(etree[1])
        ans = lookup(handle,field)
    elif etree[0] == "new": # new
        ans = interpretTTREE(etree[1])
    else :  crash(etree, "doesn't compute")
    return ans


def interpretTTREE(ttree) : # finds meaning of ttree
    if isinstance(ttree, list) :  # is it a list
        if ttree[0] == "struct" : # is it a struct
            phandle = activeNS()  
            handle = allocateNS()	
			
            namespace = lookupheap(handle)
            namespace['parentns'] = phandle
            storeheap(handle, namespace)
            interpretDLIST(ttree[1])
            deallocateNS()
            return handle
        if ttree[0] == "call" :	# is it a call
            lval = interpretLTREE(ttree[1])
            handle = lookup(lval[0], lval[1]);
            closure = lookupheap(handle)
            if closure[0] == 'class' :	#is it a class
                return interpretTTREE(closure[1])
            else :
                crash(closure[0], "isn't a class")
        else:
            crash(ttree, "isn't a struct or class")
    else :
        crash(ttree, "isn't a ttree")

def interpretLTREE(ltree) :
    """interpretLTREE computes the meaning of a lefthandside operator tree.
          LTREE ::=  ID | [ "dot", LTREE, ID ]
       post: returns a pair,  (handle,varname),  the L-value of  ltree
    """
    if isinstance(ltree, str) :  #  ID ?
        ans = (activeNS(), ltree)    # use the handle to the active namespace
    elif isinstance(ltree, list) and ltree[0] == "dot": # ["dot", LTREE, ID ]?
        handle, var = interpretLTREE(ltree[1])
        val = lookup(handle, var)
        if isLValid(val, ltree[2]):
            ans = (val, ltree[2])
        else:
            crash(ltree, val + " not in " + ltree[2])
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
    printHeap()