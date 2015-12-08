
"""Tables.py

   Table objects: dictionary of form,
   { "store": Var -> PE         # maps assigned Vars to their PE-values
     "heap" : peTuple -> Array  # maps locs of arrays to the array ob
     "rels" : retree*,          # list of facts of form,  [relop, pe, pe],
                                #    extracted from ASSERT, IF, WHILE, pre, etc
     "defs": rtree*             # list of relations about free fcn variables,
                                #   each of form,  [relop, etree1, etree2]
     "funs" : Var -> (vtreelist,btree,btree,vtree,vtreelist) 
                                # maps function name to its params, pre, post,
                                #                 answer var, and global vars
     "globalinvs" : btree*      # list of all global invariants
     "brokeninvs" : btree*      # list of all broken global invariants that
                                #  must be proved when function currently
                                #  analyzed (if any) is finished
     "novars" : vtree*          # list of global var names that current
                                # analyzed command may _not_ update
     "whoami" : Var }           # name of function currently analyzed, if any

    where  PE is a polynomial expression (a dict; see PE.py): peTuple -> int
           Array is a pair:  (PE, peTuple -> PE)

   Deep copies are made of tables, except for  funs  and  globalinvs
   which are never altered once they are entered into any table.
"""

import PE     # for access to PE.eval
import Parse  # for basic definitions of parse-tree structures
import NF     # for normal-form functions

RELOPS = Parse.RELOP   # relational operators: ==, !=, <, etc.

##############################################################

debug = False
verbose = False

def setDebug() :
    global debug
    debug = True
    PE.debug = True

def setVerbose() :
    global verbose
    verbose = True
    PE.verbose = True

##############################################################

def error(message) :
    import Scan
    print "TABLES ERROR: " + message
    Scan.write("TABLES ERROR: " + message + Scan.EOL)

##############################################################



def empty() :
    """builds and returns an empty table"""

    # funs = {"readInt" : ([], ["True"], ["isinstance", ["var", "_ans"], "int"], ["var", "_ans"], [])}
    funs = {"readInt" : ([], ["True"], ["True"], ["var", "_ans"], [])}

    return  {"store": {}, "heap": {}, "rels": [], "defs": [],  \
             "funs": funs, "globalinvs":[], "brokeninvs" : [], \
             "novars": [], "whoami": ""}


def lookupType(C6, vname):
    """looks inside C6's store to locate the data type of vname

       params: C6; vname - a string
       returns  "array" if  C6["store"][v] is a key linked to the heap
       returns  "int" if C6["store"][v] is not linked to the heap
       returns "unknown" if  v  not in store
    """
    sigma = C6["store"]
    if vname not in sigma :
        ans = "unknown"
    else :
        value = sigma[vname]
        if PE.peToTuple(value) in C6["heap"] :
            ans = "array"
        else :
            ans = "int"
    return ans


def insertAssign(C6, v, etree):
    """updates the store of C6  with an assignment. 
       If v already exists in C6's store, saves former value as  v_old
       for later use in proof reasoning.

       params: v - has form,  ["var", s]  or  ["index", ["var", s], etree]
               etree - another etree, to be assigned to the var.
    """
    sigma = C6["store"]
    heap = C6["heap"]
    badvars = C6["novars"]
    if v[0] == "var" : vtree = v
    elif v[0] == "index" : vtree = v[1]
    vold = Parse.makeOldVar(vtree)  # ["var", vname_old]

    # first, check if we are allowed to update  v:
    if (vtree in badvars) :
        error("you may not update a protected global var outside of its maintenance function")
        return

    # if possible, rename current value of var v  as  v_old:

    if v[0] == "var" and v[1] in sigma : # and lookupType(C6, v[1]) != "array":
        sigma[vold[1]] = sigma[v[1]]  # assign v's current value to v_old
    elif v[0] == "index" and lookupType(C6, v[1][1]) == "array":
        vname = v[1][1]
        loc = PE.peToTuple(sigma[vname])
        length = heap[loc][0]
        vector = heap[loc][1]
        # make copy:
        copy = {}
        for k in vector :
            copy[k] = vector[k]
        # assign original to v_old and copy to v :
        sigma[vold[1]] = sigma[vname]
        newloc = PE.make(PE.makeSym())
        sigma[vname] = newloc
        heap[ PE.peToTuple(newloc) ] = (length, copy)

    # (later,  vold  will be erased from  sigma....)
    # now, eval assignment's  rhs  and store it into  v:
    rhs = PE.evall(C6, etree)

    if v[0] == "var":  # simple var
            sigma[v[1]] = rhs
    elif v[0] == "index":   # an array/list reference
        # eval  index  expression (NOTE: no nested indexing allowed):
        indexpe = PE.evall(C6, v[2])
        # save values in sigma[vname][1] provably distinct from  vname[index]:
        vname = v[1][1]
        if vname not in sigma or lookupType(C6, vname) != "array" :
            error(vname + " is not an array in the store")
            #sigma[vname] = PE.makeArray()
        else :
            vmap = heap[PE.peToTuple(sigma[vname])][1]
            saveDistinctElements(C6, vmap, indexpe)
            vmap[PE.peToTuple(indexpe)] = rhs


def saveDistinctElements(C6, arraymap, indexpe) :
    """retains within  arraymay  only those elements provably
       distinct from  indexpe
    """
    akeys = arraymap.keys()
    for key in akeys :
        elempe = PE.tupleToPe(key)  # get pe-value of element-index
        # is the following good enough?  Or will we need theorem proving?
        distinct = PE.prove(C6["rels"], ["!=", elempe, indexpe])
        if not distinct :
            del arraymap[key]


def insertAppend(C6, v, e) :
    """appends  e  to the end of array/list  v  in the heap.
       Does the same actions as an insertAssign to an indexed array,
       but preserves more heap info since the append does not produce
       any aliases within v

       params : C6; v - a vartee; e - an etree
    """
    sigma = C6["store"]
    heap = C6["heap"]
    vname = v[1]
    vold = Parse.makeOldVar(v)
    if lookupType(C6, vname) != "array" :
        error("cannot append to a non-list/array")
    else :
        loc = PE.peToTuple(sigma[vname])
        length = heap[loc][0]
        newlength = PE.add(length, PE.make(1))
        vector = heap[loc][1]

        # assign original to v_old:
        sigma[vold[1]] = sigma[vname]

        # make copy for the new value of  v:
        copy = {}
        for k in vector :
            copy[k] = vector[k]
        newloc = PE.make(PE.makeSym())
        rhs = PE.evall(C6, e)
        copy[ PE.peToTuple(length) ] = rhs
        sigma[vname] = newloc
        heap[ PE.peToTuple(newloc) ] = (newlength, copy)


def insertAlias(C6, lhs, rhs):
    """for the purposes of tracking ``old'' and ``in'' variables,
       we copy the value of rhs and assign it to lhs in C6's store

       params: C6; lhs, rhs - vtrees of form ["var", n]
    """
    sigma = C6["store"]
    lhsname = lhs[1]
    rhsname = rhs[1]
    if rhsname in sigma :
        sigma[lhsname] = sigma[rhsname]
    else :
        #error("insertAssignCopy cannot copy a var not in the store")
        pass
    

"""
def incrementLen(C6, v, howmuch):
    updates the store of C6  by extending the length of list/array
       v by  howmuch.

       params: v - ["var", s] 
               howmuch - an int > 0
    
    sigma = C6["store"]
    heap = C6["heap"]
    vname = v[1]
    if lookupType(C6, vname) != "array" :
        error("cannot increment the length of a non-list/array")
    else :
        loc = PE.peToTuple(sigma[vname])
        length = heap[loc][0]
        map = heap[loc][1]
        heap[loc] = (PE.add(length, PE.make(howmuch)), map)
"""


def lookupGlobalInvariants(C6, varnames):
    """finds in C6 all global invariants relevant to varnames:

       params:  C6,  varnames -  a sequence of  vtrees
       returns: a list of all the invariants saved in C6 that mention
        any variable within varnames
    """
    invlist = []
    for ginv in C6["globalinvs"] :
        foundmes = map(lambda v: Parse.foundIn(v, ginv),  varnames)
        if True in foundmes :
            #invlist = invlist + (ginv,)
            invlist.append(ginv)
    return invlist

def insertGlobalInvariant(C6, inv):
    """adds  inv,  a btree, to  C6's  globals  list of global invariants
       # adds  to  gvar all vtrees (vars) embedded within inv;

       adds global invariant to  rels  and  facts, since it is now
       established, and we are not allowed to change  any of the vars
       it mentions (except from within a fcn that declars the vars
       as globals.

       finally, ``locks'' the global vars from updates, by placing
       their names on the ``novars'' list.
       Only functions that mention the vars in its ``globals''
       clause can update the global vars
    """
    C6["globalinvs"] = C6["globalinvs"] + [inv]
    globals_in_inv = Parse.removeDuplicates(Parse.extractVarsFrom(inv))
    C6["novars"] = C6["novars"] + globals_in_inv
    #erase(C6, globals_in_inv)
    reset(C6, globals_in_inv)


def insertBrokenInvariant(C6, inv):
    """adds  inv,  a btree, to  C6's  list of broken invariants
    """
    C6["brokeninvs"] = C6["brokeninvs"] + [inv]



def insertDef(C6, btree) :
    """inserts in C6's  "defs" table relation btree

       params: C6;  retree - has form  [relop, etree, etree]
    """
    C6["defs"].append(btree)


def matchDef(C6, btree) :
    """attempts to locate a defn saved in  C6["defs"] that matches
       the assert,  btree.  Returns whether or not there was success.
    """
    for scheme in C6["defs"] :
        success = Parse.match({}, btree, scheme)
        if success :  return True
    # else, no match:
    return False



def insertFunction(C6, name, params, pre, post, returnvar, globalvars):
    """inserts into C6's function table an entry for function,  name:
       C6["funs"][name] = (params, pre,post,returnvar,globalvars)

       params:  C6,  name - a vtree;  params - a vlist;  pre, post: btrees;
                returnvar: a vtree;  globalvars: tuple of vtrees (VARs)
    """
    C6["funs"][name] = (params, pre, post, returnvar, globalvars)

def getFunctionInfo(C6, funname) :
    """looksup and returns (params, pre, post, returnvar, globalvars)
       for function  funname
    """
    if funname in C6["funs"].keys() :
        ans = C6["funs"][funname]
    else : ans = ()
    return ans

def getLocalReturnInfo(C6):
    """lookup and returns the  postassert, returnvar, and broken invariants info
       for the currently analyzed function
    """
    funname = C6["whoami"]
    (params, pre, post, returnvar, globalvars) = C6["funs"][funname]
    return (post, returnvar, C6["brokeninvs"])


def insertRelation(C6, btree):
    """extracts all [RELOP, e1, e2]-relations asserted within  btree 
       and places them into the  rels  table in  C6

       params: C6 table  and  btree 
    """

    #sigma = C6["store"]
    # eval all facts in the bfactlist:
    cnffact = NF.cnf(btree)  # returns a list of disjunctive clauses
    # save any disjunctive clause that is exactly [[RELOP, b1, b2]]:
    for clause in cnffact :
        if len(clause) == 1  and  clause[0][0] in RELOPS :
            relop = clause[0][0]
            pe1 = PE.evall(C6, clause[0][1])
            pe2 = PE.evall(C6, clause[0][2])
            if pe1 != {} and pe2 != {} :
                newrel = [relop, pe1, pe2]
                if newrel not in C6["rels"] :
                    C6["rels"] = [newrel] + C6["rels"]  # new fact at front

def copy(C6) :
    """makes a deep copy of  C6  and returns it"""
    newC6 = empty()
    sigma = C6["store"]
    for key in sigma :
        newC6["store"][key] = sigma[key]

    heap = C6["heap"]
    for key in heap:
        newarray = {}
        oldarray = heap[key][1]
        for k in oldarray :
            newarray[k] = oldarray[k]
        newC6["heap"][key] = (heap[key][0], newarray)

    newC6["rels"] = [ r for r in C6["rels"]]
    newC6["defs"] = [ r for r in C6["defs"]]

    fcns = C6["funs"]
    for f in fcns :
        newC6["funs"][f] = fcns[f]

    newC6["globalinvs"] = [ g for g in C6["globalinvs"]]
    newC6["brokeninvs"] = [ g for g in C6["brokeninvs"]]
    newC6["novars"] = [ g for g in C6["novars"]]
    newC6["whoami"] = C6["whoami"]
    
    return newC6


def copyWithoutStore(C6, funname, scalars, arrays, localglobals, brokeninvariants) :
    """makes a 2-deep copy of the functions, global invariants, novars
       within  C6. 
       Used to initialize a C6 for a function body for function,  funname

       Makes store and heap empty and places dummy scalar and array values
       in store based on  scalars  and  arrays .  Sets rels to []

       Subtracts  localglobals  from  ``novars'' list to denote that
                  these vars are mutable
       Revises  globalinvs list, removing brokeninvariants that are no longer
                  invariants because their vars are mutable
       Places  brokeninvariants  into  brokeninvs list

       params: C6;  
               funname : name of function
               scalars: vtree list of scalar vars;
               arrays: vtree list of array vars
               localglobals : vtree list of global vars that can be mutated
               brokeninvariants: invariants that mention
                      local globals, a btree list
       returns new C6 configuration
    """
    newC6 = empty()

    fcns = C6["funs"]
    for f in fcns :
        newC6["funs"][f] = fcns[f]

    newC6["globalinvs"] = [ g for g in C6["globalinvs"] \
                                       if g not in brokeninvariants ] 
    newC6["brokeninvs"] = brokeninvariants

    newC6["defs"] = [ d  for d in C6["defs"] ]
    newC6["novars"] = [ g for g in C6["novars"] if g not in localglobals]
    newC6["whoami"] = funname

    for v in scalars :
        newC6["store"][v[1]] = PE.make(PE.makeSym())
    for v in arrays :
        newloc = PE.make(PE.makeSym())
        newarray = PE.makeArray()
        newC6["store"][v[1]] = newloc
        newC6["heap"][PE.peToTuple(newloc)] = newarray

    return newC6


def erase(C6, modified_vars) :
    """erases from  C6's sigma all mappings that
       mention any of the variables in the tuple,  modified_vars.

       param: modified_vars, a sequence of ["var", v]-trees
    """
    sigma = C6["store"]
    badvars = [v[1]  for v in modified_vars]
    storekeys = sigma.keys()

    for key in storekeys :
        if key in badvars :
           del sigma[key]
        #else :
        #    pe = sigma[key]
        #    if True in [ PE.foundInDeep(v, pe) for v in badvars ] :
        #        del sigma[key]


def reset(C6, modified_vars) :
    """changes  C6's sigma so that new constants are generated for
       each var mentioned in modified_vars.

       param: modified_vars, a sequence of lhs-trees; can be either
              ["var", s] or ["index" ["var", s] pe].   IMPORTANT:
              in the latter case, the  etree  has been replaced by its pe-value
    """
    sigma = C6["store"]
    heap = C6["heap"]
    #print "In reset"
    #print "store=", sigma
    for m in modified_vars :
        if m[0] == "var" and lookupType(C6, m[1]) != "array" :  # simple var
            sigma[m[1]] = PE.make(PE.makeSym())

        elif m[0] == "var" and lookupType(C6, m[1]) == "array" :
            arrayname = m[1]
            newarray = PE.makeArray()
            newloc = PE.make(PE.makeSym())
            sigma[m[1]] = newloc
            heap[PE.peToTuple(newloc)] = newarray

        elif m[0] == "index" or m[0] == "len" :
            vname = m[1][1]
            loc = PE.peToTuple(sigma[vname])
            length = heap[loc][0]
            vector = heap[loc][1]
            # make copy:
            copy = {}
            for k in vector :
                copy[k] = vector[k]
            newloc = PE.make(PE.makeSym())
            if m[0] == "index" : # indexed var ["index" ["var", s] pe]
                saveDistinctElements(C6, copy, PE.evall(C6, m[2]))
            elif m[0] == "len":  # ["len", ["var", s]], as a result of append
                length = PE.make(PE.makeSym())

            sigma[vname] = newloc
            heap[PE.peToTuple(newloc)] = (length, copy)
            


###########################################################################
# theorem prover functions:


def proveSequent(C6, bfactlist, bgoal) :
    """attempts to prove proposition  bgoal  from  sequence of propositions
       bfactlist.  
  
       params: C6; bfactlist - sequence of btrees; bgoal - a btree

       Approach:  places  bgoal into cnf; 
                  places conjucntion of bfactlist into dnf;
                  for each subgoal in cnf, for each sublist in dnf,
                    attempts to prove  sublist |- subgoal.
                  If all are accomplished, then goal is proved.
       returns True, if bgoal proved; returns False otherwise
    """
    #if bgoal[0] == "forall" :
    #    success = proveUniversal(C6, bfactlist, bgoal)  # sorry...
    #    return success

    # place  bfactlist  into  dnf to compute all possible proof contexts:
    bigfact = NF.conjunctionOf(bfactlist)
    dfacts = NF.dnf(bigfact)   # all possible cases in bfactlist

    subgoals = NF.cnf(bgoal)   # must prove all subgoal conjuncts

    for subg in subgoals :  # must prove each subgoal,  subg
        if ["True"] in subg :   # each subg is a disjunct...
            pass  # it's proved
        else :
            for premiselist in dfacts :  # must prove each  premiselist |- subg
                #print "READY TO PROVE:", premiselist
                #print "|-", subg
                #print
                if ["False"] in premiselist :
                    pass # proved -- the premises are self-contradictory
                else : # rats, time to do a proof:
                    # since subg is a disjunction, use  premiselist
                    # to try to prove _one_ of the disjuncts:
                    proved_subg = False
                    for prim in subg :
                        proved_subg = verifyRelation(C6, premiselist, prim)
                        if proved_subg : break  
                    if not(proved_subg) : return False  # we failed

    return True  # we made it this far; it means all subgoals were
                 # proved with all possible premiselist combinations.


def verifyRelation(C6, bfactlist, bgoal) :
    """attempts to verify  bgoal,  which is a primitive (relop or forall)
       
       params: C6 table
               bfactlist: a list of facts of form
                  [relop, e1, e2]  or  [forall/exists, lo, i, hi, e]
               bgoal: a single fact of form [relop, e1, e2]
                                         or [forall/exists, lo, i, hi, e]

       returns : True, if  bfactlist |- bgoal  is proved
                 False, if not
    """
    #print "verifyRelation: C6"#, C6
    #print "bfactlist:",  bfactlist
    #print "bgoal:", bgoal
    #raw_input("press Enter")

    if (bgoal[0] in RELOPS) :   # [relop, e1, e2]
        # eval goal:
        pe1 = PE.evall(C6, bgoal[1])
        pe2 = PE.evall(C6, bgoal[2])
        goal = [bgoal[0], pe1, pe2]

        # eval all facts in the bfactlist:
        factlist = []
        for f in list(bfactlist) :
            if f[0] in RELOPS :
                pe1 = PE.evall(C6, f[1])
                pe2 = PE.evall(C6, f[2])
                factlist.append([f[0], pe1, pe2])
            elif f[0] in ("forall", "exists") :
                 pass # can't handle quantified phrases (yet) in PE!
                 # If I am brave, I might try to evaluate lower and upper
                 # bounds of quantification and enumerate the facts therein.
                 # But this is high overhead....
        # send off the PE-valued facts and goal to the prover:
        #print "In verifyrelation; ready to call PE.prove:"
        #print "all facts=", factlist + C6["rels"]
        #print "goal=", goal
        return PE.prove(factlist + C6["rels"], goal)
    elif bgoal[0] == "forall" :
        return proveUniversal(C6, bfactlist, bgoal)
    else :  # ["exists", lo, i, hi, e] ???
        return False


def proveUniversal(C6, bfactlist, bgoal) :
    """ Tries to prove a bgoal of form,   ["forall", lo, i, hi, bprop_i_]
        from  bfactlist.   First, attempts to show  hi <= lo,  meaning
        quantification ranges over empty set.   If this fails, tries
        to establish numerical lower and upper bounds for the quantification
        and enumerate proofs for all elements within these bounds.
        If this fails, then searches
        for a  bfact in bfactlist that is a forall of the same form,
        but where its upper bound is  hi-1.   If success, then tries
        to prove  bprop_hi-1_.

        If I have the energy, I'll try to make this smarter later....
    """
    #print "proveUNIVERSAL: bfactlist=", bfactlist
    #print "goal=", bgoal
    lo = bgoal[1]
    hi = bgoal[3]
    i = bgoal[2]
    bprop = bgoal[4]

    # first, see if  bgoal in premises:
    success = bgoal in bfactlist

    if not success :
        # next, try to prove that domain is empty, ie, hi <= lo :
        success = verifyRelation(C6, bfactlist, ["<=", hi, lo])

    if not success:
        # next, try to establish numerical lower and upper bounds and
        # prove  bprop  for all elements in the numerical range:
        lonum = PE.evallToInt(C6, lo)
        hinum = PE.evallToInt(C6, hi)
        if isinstance(lonum, int)  and  isinstance(hinum, int):
            success = True  # so far, so good...
            for j in range(lonum, hinum):
                stree = Parse.substituteTree(["int", str(j)], i, bprop)
                success = success and proveSequent(C6, bfactlist, stree)

    if not success:
        # then search bfactlist for a forall goal whose body
        #  matches  bprop and whose bounds cover  bgoal's all but one:
        possibles = [ f for f in bfactlist
                      if f[0] == "forall" \
                         and Parse.substituteTree(i, f[2], f[4]) == bprop \
                         #and verifyRelation(C6, bfactlist, ["==", f[1], lo]) \
                         and verifyRelation(C6, bfactlist, ["<=", f[1], lo]) \
                         and verifyRelation(C6, bfactlist,  \
                                     ["==", ["+", f[3], ["int", "1"]], hi]) \
                    ]
        if len(possibles) > 0 :
            success = proveSequent(C6, bfactlist, 
                                   Parse.substituteTree \
                                       (["-", hi, ["int", "1"]], i, bprop) )

    if not success:
        #search bfactlist for a forall goal whose body
        #  matches  bprop and whose bounds cover  bgoal's:
        possibles = [ f for f in bfactlist
                      if f[0] == "forall" \
                         and Parse.substituteTree(i, f[2], f[4]) == bprop \
                         and verifyRelation(C6, bfactlist, ["<=", f[1], lo]) \
                         and verifyRelation(C6, bfactlist, [">=", f[3], hi]) \
                    ]
        success = (len(possibles) > 0)

    return success
