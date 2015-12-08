
"""PE
   Holds algorithms for building and operating on polynomial expressions.

   Format of PE objects: 
     SVar -> int    a dictionary
     SVar =  tuple of (tuples of) strings (var names) and ints,
               ordered lexicographically

   Example:  2*y*x - y + 3  is represented as
                            { ("x","y"): 2,  ("y"):-1,  ():3 }


   Unresolved function calls (as what one might find inside a spec)
   are ``Skolemized'' into a tuple that is used as a key in the PE value:

   Examples:  2*f(i)   is  { ("f", ((("i",)1),((),0)) ): 2,  (): 0 }
                       because the PE-value of  i  is  {("i",):1, ():0}
          f(4i+8,9) + 1   is  { ("f", ((("i",)4),((),8)), ((),9)): 1,  (): 1 }


   Here is the syntax of PE-values:
   PE ::= { (VARK,*): int * }  <-- dict. of varlists to coefficients
   VARK ::= string  |  (string,PETUPLE)   <-- simple vars and indexed vars
   PETUPLE ::= ( VARVAL,*)   <-- flattened dictionary
   VARVAL ::= ((VARK,*),int)   <-- flattened  varlist, coefficient pair

   Operations supported on PE objects:
      addition, subtraction, multiplication
      attempted relational comparisons of PE values
      evaluation of EXPR optrees to PE values
"""

import Parse

# INVARIANT: all PE-values contain the () key.  (no empty dictionaries here)

debug = False
verbose = False

MAXTRIES = 100  # max iteration attempts to prove any single numerical relation

integer_arithmetic = True  # should theorem prover assume that all unknowns
                           # denote integers ?  (useful to prove, say,
                           #  x > k  |-  x-1 >= k  )

def make(n):
    """makes the PE constant, n.
       param: n.  If n is an int,  makes  {():n}
                  If n is anything else (i.e., a key), makes  {(n,):1}
       returns the constant
    """
    if isinstance(n, int) : ans = {():n}
    else :  ans = {(n,):1, ():0}
    return ans


# sample values for science experiments:
ZERO = make(0)
ONE =  make(1)
TWOX = { ("x",):2, ():0 }
XSQ =  { ("x","x"):1, ():0 }
X1SQ = { ("x","x"):1, ("x",):2,  ():1 }

###############################################################

def error(message) :
    import Scan
    print "PE ERROR: " + message
    Scan.write("PE ERROR: " + message + Scan.EOL)

##############################################################

# functions that manipulate keys:

def sortedKey(k):
    """returns a new key that has same items in it as  k  but sorted"""
    klist = list(k)
    klist.sort()
    return tuple(klist)

def peToTuple(pe) :
    """flattens pe, a PE-value (dict.) to a nested tuple. See comments
       at top of this file.
    """
    pairs = [ (k, pe[k])  for k in pe.keys() ]
    pairs.sort()
    return tuple(pairs)

def tupleToPe(nestedtuple):
    """inflates nested tuple of key,value pairs into a dictionary (PE-value)"""
    ans = make(0)
    for pair in nestedtuple :
        ans[pair[0]] = pair[1]
    return ans
    

#########################################################################

# functions that manipulate PE-values:

def copy(pe) :
    """copies  pe in a new PE-object and returns it"""
    ans = {}
    for k in pe.keys():
        ans[k] = pe[k]
    return ans


def substituteDeep(replacement, pattern, pe):
    """returns a new PE-value that looks like  pe  except that all 
       occurrences of pattern in the keys are replaced by replacement
       Keys are replaced deeply, e.g.,
           substituteDeep("b", "a", {("a",("r","a")): n} )
              returns  {("b",("r","b")): n}
    """
    def newKey(rep, pat, k) : 
        """builds new key, [rep/pat]k, for tuple, k """
        newk = ()
        for vname in k :
            if vname == pat :
                newk = newk + (rep,)
            elif isinstance(vname, tuple) :
                newk = newk + (newKey(rep, pat, vname),)
            else :
                newk = newk + (vname,)
        return newk

    ans = {}
    for k in pe.keys() :
        ans[newKey(replacement,pattern,k)] = pe[k]
    return ans    


def foundInDeep(pattern, pe):
    """returns True iff an instance of  pattern  is found within any key in
       PE-value pe.  Does a deep search to accommodate array-index expressions.

       param: pattern: a string or tuple that can be used as a key
          pe - PE-value, whose keys are tuples (of tuples) of strings and ints
    """
    def foundInKey(pat, k):
        """searches for  pat  within nested tuple  k"""
        if pat == k :
            return True
        elif isinstance(k, tuple) :
            subsearches = [ foundInKey(pat, subk) for subk in k]
            if True in subsearches :
                return True
        else : return False

    searches = [foundInKey(pattern, k) for k in pe.keys()]
    return (True in searches)


def removeZeros(pe) :
    """mutates PE value  pe  by deleting all entries of form,  pe[k] = 0,
       E.g.,  { ("x",):0, ():3 } is just  {():3 }.
    """
    keylist = pe.keys()
    for k in keylist :
        if k != () and pe[k] == 0 :
            del pe[k]
    return pe  # now that it's mutated



##################################################################

# polynomial arithmetic operations.  Tedious but crucial....


def add(pe1, pe2):
    """returns a new PE-value that is the sum of PE-values,  pe1 and pe2.
       It's easy: add coefficients for all matching keys in pe1 and pe2.
    """
    ans = make(0)
    for k in (set(pe1.keys()) | set(pe2.keys())) :  #union of pei key sets
        if k in pe1  and  k in pe2 :
            ans[k] = pe1[k] + pe2[k]
        elif k in pe1 :  # and not k in pe2 --- treat as  pe2[k] == 0
            ans[k] = pe1[k]
        elif k in pe2 :  # and not k in pe1 --- treat as  pe1[k] == 0
            ans[k] = pe2[k]
        else :
            error("an impossible key error occurred at add")
    return removeZeros(ans)

def negate(pe):
    """returns a new PE-value that is the negation of PE-value,  pe"""
    ans = {} 
    for k in pe.keys() :
        ans[k] = 0 - pe[k]
    return ans

def subtract(pe1, pe2):
    """returns a new PE-value that is the difference of pe1 and pe2"""
    return add(pe1, negate(pe2))

#####

def addInto(pe1, repository) :
    """adds all the values within PE-value, pe1, into PE-value,  repository"""
    for key in pe1 :
        if key in repository :
            repository[key] = repository[key] + pe1[key]
        else :
            repository[key] = pe1[key]
        
def mult(pe1, pe2):
    """returns a new PE-value that is the product of PE-values,  pe1 and pe2

       Does polynomial multiplication:
         for pe1 = (c0*x0 + c1*x1 + ...),
             pe2 = (d0*y0 + d1*y1 + ... ),
         pe1 * pe2 ==  pe1*d0*y0  +  pe1*d1*y1  +  ...
         where 
          (c0*x0 + c1*x1 + ...)*dk*yk ==  c0dk*x0yk  +   c1dk*x1yk  +  ...
            that is, we must build new keys,  x0yk, x1yk, etc., for the answer
    """
    sumlist = []  # will hold the summands; see above comment
    for k in pe2.keys() :
        # compute  pe1 * pe2[k] :
        ansjk = make(0)
        for j in pe1.keys() :   
            # compute  pe1[j] * pe2[k] --- build new key and multiply:
            ansjk[sortedKey(j+k)] = pe1[j]*pe2[k]
        # collect summands
        sumlist.append(ansjk)
    # add summands:
    ans = make(0)
    for summand in sumlist :
        addInto(summand, ans)
    return removeZeros(ans)


#########################################################################

# how to eval an EXPR optree into its PE-value:

symcount = -1  # a counter for gensyms
def makeSym() :
    global symcount
    symcount = symcount + 1
    return  "_c" + str(symcount)

def makeArray():
    newlen = make(makeSym())
    return (newlen, {})


def evall(C6, etree):
    """evaluates etree into PE format,  using  store and heap in C6

       params:  C6;  etree in usual form, defined in Parse.py
       returns : resulting  PE-value.  If etree is malformed or
         evall gets lost, it returns {}
    """
    ans = {} 
    # case on structure of etree:
    op = etree[0]
    if op == "var" :  # etree is  ["var", vname],  where  vname is a string(!)
        store = C6["store"]
        vname = etree[1]
        if vname in store :
            ans = store[vname] 
        else :  # invent a dummy name for the var and return it...
            #newvalue = make(makeSym())
            #store[vname] = newvalue
            #ans = newvalue # {(_cn,):1, ():0}  # is a free var
            if verbose :
                print "WARNING: evall couldn't find var " + vname + " in the store"
    elif op == "int" :  # etree is ["int", "n"]
        ans = make(int(etree[1]))  
    elif op == "readInt" :
        ans = make(makeSym())   # it's an unknown, new input int
    elif op == "index": # ["index", ["var", v], etree]
        arrayloc = peToTuple(evall(C6, etree[1]))  # get loc of array in heap
        if arrayloc in C6["heap"] :
            vector = C6["heap"][arrayloc][1]
            index = peToTuple(evall(C6, etree[2]))  # PE val to tuple rep.
            if index in vector :   # lookup  listname[index]
                ans = vector[index]
            else :
                # can't find index in  vector,  so try to prove index
                # equal to an existing key:
                listkeys = vector.keys()
                indexpe = tupleToPe(index)
                alias = {}
                for key in listkeys :
                    keype = tupleToPe(key)
                    found = proveRELATION(C6["rels"], ["==", keype, indexpe])
                    if found :
                        alias = key
                        break
                if alias != {} :
                    ans = vector[alias]
                else :
                    if verbose :
                        print "WARNING: evall could not resolve " + etree[1][1] +  str(etree[2]) + " in the store.  Will fake it."
                    newvalue = make(makeSym())
                    vector[index] = newvalue
                    ans = newvalue
        else :
            error("scalar or unknown var " + Parse.tostringExpr(etree[1]) + " cannot be indexed")
    elif op == "len" :   # etree is  ["len", vtree]
        arrayloc = peToTuple(evall(C6, etree[1]))  # get loc of array in heap
        if arrayloc in C6["heap"] :
            ans = C6["heap"][arrayloc][0]
        else :
            if verbose :
                print "WARNING: evall couldn't find array " + etree[1][1] + " in the store"
    elif op == "list" : # etree is ["list" etreelist ] --- const array
        newvector = {}
        elems = [ evall(C6, e) for e in etree[1] ]
        for i in range(len(elems)) :
            newvector[peToTuple(make(i))] = elems[i]
        newloc = make(makeSym())  # for now, we treat locns  like ints
        C6["heap"][peToTuple(newloc)] = (make(len(elems)), newvector)
        ans = newloc # built a new array

    elif op == "call" :  # etree is ["call", v, etreelist ]
        # makes a ``skolem constant'' out of the call --- does NOT evall call
        fname = etree[1]
        args = [ peToTuple(evall(C6, e)) for e in etree[2] ]
        # build key, (fname, arg0, arg1, ..., argn), and make a PE value for it:
        ans = make( (fname,) + tuple(args) )
    
    elif op == "+" :  #  etree is  {"+", e1, e2]
        pe1 = evall(C6, etree[1])
        pe2 = evall(C6, etree[2])
        ans = add(pe1, pe2)   # places sum of pe1 and pe2 into ans
        """ SORRY-- can no longer do list addition/append this way:
        elif isinstance(pe1, tuple) and isinstance(pe2, tuple) : # both lists
            len1 = pe1[0]  # length of first list
            anslen = add(len1, pe2[0])  # length of combined lists
            ansmap = {}
            for k in pe1[1].keys() :
                ansmap[k] = pe1[1][k]  # copying items in pe1 list into ans
            for k in pe2[1].keys() :
                newkey = peToTuple(add(len1, tupleToPe(k)))
                ansmap[newkey] = pe2[1][k]
            ans = (anslen, ansmap)
        else :
            error("adding arrays and ints")
        """

    elif op == "-" :  # etree is  ["-", e1, e2]
        pe1 = evall(C6, etree[1])
        pe2 = evall(C6, etree[2])
        ans = subtract(pe1, pe2)
    elif op == "*" :  # etree is  ["*", e1, e2]
        pe1 = evall(C6, etree[1])
        pe2 = evall(C6, etree[2])
        ans = mult(pe1, pe2)
    else : # the expression is not an int-typed expr, and we are lost
        error("evall cannot evaluate this non-int expr: " + str(etree))
    return ans


def evallToInt(C6, etree):
    """evalls param  etree to see if it is a concrete int.

       params: C6; etree 
       returns: the int value of  etree, if  evall computes one;
                (), if  etree computes to a PE-value with a var in it
    """
    value = evall(C6, etree)
    if isinstance(value, dict) and value.keys() == [()] :
        ans = value[()]  # get numerical coefficient
    else : ans = ()      # not a const value
    return ans
        

#######################################################################

# functions for proving relations,  pe1 relop pe2


RELOPS = ("==", "!=", "<", "<=", ">", ">=")
LTOPS = ("<", "<=", ">", ">=")

# dictionaries that define elementary games on relational operators:
negationOf = {"==": "!=", "!=": "==", "<": ">=", "<=": ">", ">": "<=", ">=": "<"}
rotate = {"==": "==", "!=": "!=", "<": ">", "<=": ">=", ">": "<", ">=": "<="}


def prove(factlist, goal):
    """attempts to validate goal using the facts in factlist

       parame: factlist - a sequence of relational-expr facts, of form,
                          [RELOP, pe1, pe2]
               goal - a single relational-expr fact of form  [RELOP, pe1, pe2]
      returns a boolean, signifying success or failure
    """
    if goal[0] in RELOPS :
        return proveRELATION(factlist,goal)
    else : return False


def findUsefulCommonVar(subgoal, pe) :
    """searches for a possible cross multiplication between
          subgoal op 0   and  0 op' pe
       that reduces the number of free vars in  subgoal  by at least
       one common var,  v

       params:  subgoal and  pe  are PE-values. see above sentence.

       If conditions are satisfied, then returns the coefficients,
       swapped, for cross multiplication: returns  (pe[v], subgoal[v])
       If not, returns (0,0).
    """
    def gcd(a,b) :  # a quick gcd function
        while a :
            a,b = b%a,a
        return b

    ans = (0,0)
    pekeys = pe.keys()
    if () in pekeys : pekeys.remove(())
    commonkeys = [ k for k in pekeys if k in subgoal.keys()]
    if len(commonkeys) > 0 : 
        anskey = commonkeys[0]
        #ans = (pe[anskey], subgoal[anskey])
        coeff1,coeff2 = (pe[anskey], subgoal[anskey])  # get coefficients
        factor = gcd(coeff1,coeff2)  # compute their gcd
        # return minimal coefficent pair that ensure cancellation
        ans = (coeff1/factor, coeff2/factor) 
    # else, no match, so
    return ans


def crossMultiply(c1, c2, subgoal, fact):
    """performs cross multiplication of subgoal and fact:
       pre: subgoal = [sop, s1, ZERO]
            fact = [fop, ZERO , f2]
       computes and returns,   [ansop, c1s1, c2f2]
       (If either c1 or c2 are <0, then args are flipped in in either
       subgoal or fact.  See code.)
 
       Also returns boolean as to whether the multiplication eliminated a var
    """
    OKrelsFor  = { "<" : ("<", "<=", ">", ">=", "=="),
                   "<=" : ("<", "<=", ">", ">=", "=="),
                   ">" : ("<", "<=", ">", ">=", "=="),
                   ">=" : ("<", "<=", ">", ">=", "=="),
                   "!=" : ("==",),
                   "==" : ("==", "!=", ">", ">=", "<", "<=") }

    ADDOPS = { ("==","=="): "==",  \
               ("==","!="): "!=", ("!=","=="): "!=", \
               ("==", ">="): ">=",  (">=", "=="): ">=",  \
               ("==", ">"): ">",  (">", "=="): ">",  \
               (">=", ">"): ">",  (">", ">="): ">",  \
               (">=", ">="): ">=",  \
               (">", ">"): ">" }

    subgoalop = subgoal[0]
    factop = fact[0]

    # multiply subgoal by c1:
    subs_zero_is_at = +1    # remember that ZERO is on rhs of subgoal
    if c1 < 0  and  subgoalop in LTOPS :
        sargs = (subgoal[2], subgoal[1])  # must flip for  >, >=  relops
        subs_zero_is_at = -1              # ZERO got moved to lhs
    else :
        sargs = (subgoal[1], subgoal[2])
    c1sargs = ( mult(sargs[0], make(c1) ), mult(sargs[1], make(c1)) )

    # multiply fact by c2:
    facts_zero_is_at = -1 #remember that ZERO is on lhs of fact
    if c2 < 0 and factop in LTOPS  :
        fargs = (fact[2], fact[1])
        facts_zero_is_at = +1
    else :
        fargs = (fact[1], fact[2])
    c2fargs = ( mult(fargs[0], make(c2)), mult(fargs[1], make(c2)) )

    # To cancel the common variable, we must have symmetry:
    #   sargs  and  fargs  must have ZERO in opposite positions.
    #   if they don't, rotate one of em to make it so:
    good_to_go = True
    if (subs_zero_is_at + facts_zero_is_at) != 0 :  
        # must rotate either  c1sargs or c2fargs  to cancel variable:
        if subgoalop in ("==", "!=") :
            c1sargs = (c1sargs[1], c1sargs[0])
        elif factop in ("==", "!=") :
            c2fargs = (c2fargs[1], c2fargs[0])
        else :  # we are lost --- neither relation can be rotated;
                # the cross multiplication will not cancel the common var....
            return (False, [])

    # special case for inferring  val >= 0,  0 != val  |- val > 0 :
    if ">=" in (factop, subgoalop)  and  "!=" in (factop, subgoalop) \
       and c1sargs[0] == c2fargs[1]  and  c1sargs[1] == c2fargs[0] :
        if factop == ">=" :
            if c2fargs[0] == ZERO : ansarg = negate(c2fargs[1])
            else : ansarg = c2fargs[0]
        else :  # subgoalop == ">=" 
            if c1sargs[0] == ZERO : ansarg = negate(c1sargs[1])
            else : ansarg = c1sargs[0]
        return (True, [">", ansarg, ZERO])

    # Else, attempt usual monotone addition of two relations:
    if factop not in OKrelsFor[subgoalop] :
        return (False, [])
    # Else, add em together:
    rop = ADDOPS[(subgoal[0], fact[0])]
    return (True, [rop, add(c1sargs[0], c2fargs[0]),  add(c1sargs[1], c2fargs[1])])


def proveRELATION(factlist, goal):
    """attempts to validate  goal = [relop, pe1, pe2]  with factlist,
       which is itself a list of  [relop, pe1, pe2] items.

       Proceeds by negating goal and checking invalidity.
       If not invalid, uses facts in factlist (and cross multiplication)
       to eliminate vars in the goal until an invalidity is demonstrated
       (or we run out of useful facts in factlist to apply)

       returns boolean outcome of invalidity check.
    """
    #print
    #print "HELLO.  in proveRELATION. goal=", goal
    #print "factlist=", factlist
    #print "HERE WE GO:"
    notrelop = negationOf[goal[0]]
    if notrelop in ("<", "<=") :
        subgoal = [rotate[notrelop], goal[2], goal[1]]
    else :
        subgoal = [notrelop, goal[1], goal[2]]
    # assert: subgoal has relop that is  >,  >=, ==, or !=
    # Now we try to refute subgoal, ie, the negated goal:
    (success, subgoal) = refuteREL(subgoal) 
    # assert: subgoal is now [relop, pe, ZERO]

    # We employ a worklist algorithm:
    worklist = [subgoal] + [ f for f in factlist ]
    database = factlist + [subgoal]
    attempts = 0   # we will track how many attempts we make to prove it...
    while not success and worklist != [] and attempts != MAXTRIES :
        #print
        #print "database=", database
        #print "worklist=", worklist
        #print
        #raw_input("Press enter")
        attempts = attempts + 1
        s = worklist[0]   # get next subgoal to analyze
        # normalize  s  to format,  [relop, etree, ZERO]:
        sop = s[0]
        if sop in ("<", "<="):
            s = [rotate[sop], s[2], s[1]]  # it's > or >=
        spe = subtract(s[1], s[2])
        s = [s[0], spe, make(0)]
        # assert:  subgoal has form,  [relop', spe, ZERO]

        # here are some hacks for exploiting integers:
        if integer_arithmetic :
            if s[0] == ">" : # and spe[()] == 1 :
                # so,  s > 0  |-  s-1 >= 0
                auxs = [">=", subtract(s[1], make(1)), s[2]]
                if auxs not in database :
                    worklist.append(auxs)
                    database = [auxs] + database

        worklist = worklist[1:]
        for f in factlist :
           #print "fact=", f,  "subgoal=", s
           (success, newsub) = match(f, s)
           if success : break  # proved it; no need to continue
           #print "success, newsub=",  success, newsub
           # else, not success, but maybe we have a useful subgoal:
           if  newsub != [] and  newsub not in database :
               #print "failed, but adding newsubgoal=", newsub
               worklist.append(newsub)
               database = [newsub] + database
    #print "QUIT LOOP!",  success
    if attempts == MAXTRIES :
        print "PE Warning: solver exhausted --- proof attempt failed!"
    return success           

def match(fact, subgoal):
    """does resolution step between fact and subgoal
       returns  boolean and new subgoal (if boolean is True)

       pre:  fact and subgoal are relational trees of form [relop, pe, pe]
             subgoal has form,  [==/!=/>/>=, pe, ZERO]
    """
    factop = fact[0]
    if factop in ("<", "<="):
        fact = [rotate[factop], fact[2], fact[1]]  # now, it's > or >=
    pe = subtract(fact[2], fact[1])
    fact = [fact[0], make(0), pe]
    # assert:  fact has form,  [relop', ZERO, pe]

    """
    subgoalop = subgoal[0]
    if subgoalop in ("<", "<="):
        subgoal = [rotate[subgoalop], subgoal[2], subgoal[1]]  # it's > or >=
    spe = subtract(subgoal[1], subgoal[2])
    subgoal = [subgoal[0], spe, make(0)]
    # assert:  subgoal has form,  [relop', spe, ZERO]
    """
    # Attempt a variable-elimination step on non-ZERO parts:
    (c1, c2) = findUsefulCommonVar(subgoal[1], fact[2])
    #print "c1, c2=", c1, c2
    if (c1,c2) != (0,0) :
        (ok, subgoal) = crossMultiply(c1,c2,subgoal,fact)
        #print "subgoal after mult is", subgoal 
        if ok :
            return refuteREL(subgoal)  # did it work?
        else :
            return (False, [])
    return (False, [])
    


def refuteREL(goal):
    """reformats the goal, [relop, pe1, pe2],  into   [relop, (pe1 - pe2), 0]
       and checks whether this relation is invalid. (It does so by
       checking whether (pe1 - pe2) has form, {():v}  and  (v relop 0) fails.)
    
       params:  goal = [relop, pe1, pe2],  relop in (">",">=","==","!=")
       returns: a pair -
           (i) the result of the invalidity check:
              True means goal is invalid (and the proof of contradiction
                   succeeded).  False means no decision yet.
           (ii) [relop, (pe1 - pe2), ZERO]
    """

    # comparison functions, organized as a table:
    compare = { ">": (lambda x,y: x>y),   ">=": (lambda x,y: x>=y),  \
               "==": (lambda x,y: x==y),   "!=": (lambda x,y: x!=y) }

    relop = goal[0]
    pe3 = subtract(goal[1], goal[2])
    subgoal = [relop, pe3, make(0)]
    pe3keys = pe3.keys()
    if pe3keys == [()] :
        success = not(compare[relop](pe3[()], 0))
    else :
        success = False
    #print "refuteREL: success=", success, "p3=", pe3
    return (success, subgoal)

