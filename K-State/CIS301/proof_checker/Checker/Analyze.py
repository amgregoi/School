
"""Python program analyzer.  Reads the lines of an annotated Python
   program and checks all embedded Hoare-style program proofs.

   Key internal data structures:
     --- C6 : a table holding assignment, information about relational
              assertions,  function names and their pre-post-conditions,
              and global-variable invariants (structure defined in  Tables.py)

     --- premises = a tuple of btrees that are active and can be
            used in the next proof embedded in the program
            (see Parse.py for structures of  btrees)

   Basic algorithm:

   ask Scan to read next source-program line
   repeat until EOF:
      ask Parse to parse the line
      decode the parsetree and call appropriate  analyzeXXX function,
          which checks asserts and writes output program
      ask Scan to read next source-program line

   Because Python is line oriented, the  analyzeXXX functions are
   part parser (for multi-line loops and conditionals and proofs)
   and part semantic analyzer.

   IMPORTANT NOTE: algebra theorem prover is "tuned down" in this code
                   can tune precision in  checkProof
"""

import Scan
import Parse
import Tables

########################################################################

# global variables: the current source program line,
# represented in its original text, its leading indentation whitespace,
# and its tokens, a tuple:
textline = ""   # string holding current source command and preceding whitespace
indent = ""     # a string holding exactly the whitespace for command line
tokens = ()     # a tuple of strings --- words --- from the textline

EOF = Scan.EOF
EOL = Scan.EOL

debug = False  # remembers if breakpoints should be activated
verbose = False # remembers whether to display internal info in output file
function_asserts = False # remembers whether to generate  python ASSERTs
                         # for each function's precondition
                         # as well as header code for execution
all_asserts = False # remembers whether a proof fragment should forward
                    # all premises given to it as input as well as the
                    # conclusion asserts it proved

assert_errors = False  # remembers if analyer inserted its own ASSERTS


def resetGlobals() :
    """sets above globals to their defaults"""
    global textline, indent, tokens, debug, verbose, function_asserts, all_asserts, assert_errors
    textline = ""
    indent = ""
    tokens = ()
    debug = False
    verbose = False
    function_asserts = False
    all_asserts = False
    assert_errors = False


def getNextLine() :
    """read the next line of program text: """
    global textline, indent, tokens
    (textline, indent, tokens) = Scan.readLine()


###########################################################################
# routine functions for making strings and writing to output file:

def writeText(text) :
    """writes text, as is, to output file"""
    Scan.write(text)

def writeTextList(indent, codelist):
    """formats and writes a sequence of codelines to output file"""
    for line in codelist :
        Scan.write(indent + line + EOL)

def writeTextLists(myindent, mytextline, unproved_asserts, annotated_proof) :
    """formats and writes a block of code to output file:

       myindent:  leading whitespace
       mytextline: one raw textline --- source-program text
       unproved_asserts: a tuple of btrees that must be formatted as
         ASSERT commands and printed
       annotated_proof: a tuple of raw textlines to write

       Last three params are printed, in order
    """
    writeText(mytextline)
    writeTextList(myindent, formatUnprovedAsserts(unproved_asserts))
    for line in annotated_proof :
        writeText(line)

def formatUnprovedAsserts(assert_tuple):
    """builds a tuple of ASSERT commands for the btrees in assert_tuple"""
    #print "formatAsserts called with:", assert_tuple
    return map(lambda btree: formatUnprovedAssert(btree),  assert_tuple)

def formatAsserts(assert_tuple):
    """builds a tuple of ASSERT commands for the btrees in assert_tuple"""
    #print "formatAsserts called with:", assert_tuple
    return map(lambda btree: formatAssert(btree),  assert_tuple)

def formatAssert(btree):
    bstring = Parse.tostringBexpr(btree)
    return "assert " + bstring

def formatUnprovedAssert(btree):
    global assert_errors
    assert_errors = True
    bstring = Parse.tostringBexpr(btree)
    print "UNABLE TO VERIFY " + bstring
    return "assert " + bstring + "  # UNABLE TO VERIFY"

def insertPrecode(precode_list, textline) :
    """inserts sequence of precode strings as the penultimate line in
       multiline string,  textline,  and returns it
    """
    insertpoint = textline.rfind(EOL,0,len(textline)-1)
    precode = ""
    for cmd in precode_list :
        precode = precode + cmd
    ans = textline[:insertpoint+1] + precode + textline[insertpoint+1:]
    return ans

def makePrecode(C6, myindent, varpairlist) :
    """generates precode assignments,  "v_old = v",  or
       "v_old = [ a for a in v ]",  for each  (v_old,v) in varpairlist
       and returns the list of assignments
       params:  myindent - the amount of needed indentation
               varpairlist:  list of pairs of strings
    """
    # make list of assignments for the unproved properties of the old_vars:
    precode = []
    for pair in varpairlist:
        (voldname, vname) = pair
        if Tables.lookupType(C6, vname) == "array" :
            precode.append( myindent + voldname + \
               " = [ _v for _v in " + vname + " ]" + EOL )
        else :
            precode.append( myindent + voldname + " = " + vname + EOL )
    return precode

######################################################################

"""IMPORTANT:  all analyzeXXX functions operate
  under global invariant that  textline, indent, and tokens  hold
  the next, fresh line to be processed.  The functions assume this on
  entry and preserve it on exit.

  BUT checkProof does not preserve this property on exit!!!
  This is because the formatting of the output program must be driven
  by the  analyzeXXX  functions.
  
  All analyzeXXX functions take three args:
     C6 tables
     premises (a tuple of btrees), the active premises at this program point
     optree (parse tree) of phrase form being analyzed

  All fuctions return a pair:
     a tuple of the asserts that are premises for the next command line
     a tuple of any program vars that were modified by the phrase analyzed
"""


def analyzePASS(C6, premises, optree) :
    """analyzes the current text line, a PASS
        
       params:  C6: constraint tables;  premises: premise tuple of btrees;
                optree: parse of current text line: ["assert", btree]
    
       returns: premises and empty tuple of updated vars
    """
    writeText(textline)
    getNextLine()
    """
    if len(premises) > 1 :
        newpremises = premises[:1]
    else :
        newpremises = ()
    return (newpremises, ())  
    """
    return (premises, ())


def analyzeASSERT(C6, premises, optree) :
    """analyzes the current text line, an ASSERT
       
       params:  C6: constraint tables;  premises: premise tuple of btrees;
                optree: parse of current text line: ["assert", btree]

       updates  C6  with this assert and subsequent proved consequences

       returns: premises + the new assertion  and empty tuple of updated vars
    """
    writeText(textline)
    relexpr = optree[1]

    # check btest for well-formedness:
    #OLD Tables.checkTest(C6, relexpr)

    Tables.insertRelation(C6, relexpr)
    newpremises = (relexpr,) + premises
    getNextLine()
    return (newpremises, ())



def analyzeASSIGN(C6, premises, optree) :
    """analyzes the current text line, an ASSIGN
       
       params:  C6: constraint tables;  premises: premise tuple of btrees;
                optree: parse of current text line: ["=", V, etree]
                   where  V is ["var", string]  (for now)

       updates  C6  with consequences of the ASSIGNMENT proof law

       returns: finalAssertionOfProof and singleton of modified var: (V,)
                (if no proof is attached to assign, then consequences from
                 the assignment proof law are returned)
    """
    breakpt("entered analyzeASSIGN", C6, [("optree=", optree)])
    mytextline = textline  # holds the source textline of the assignment
    myindent = indent      # needed if we must generated additional code here

    v = optree[1]
    e = optree[2]

    precode = ()           # holds assigns and asserts generated by analysis
    modified_vars = (v,)    # vars modified by this assignment

    # define  vartree,  which is the  ["var",s] part of the lhs:
    if v[0] == "var" :   # is the var a simple var?
        vartree = v
    elif v[0] == "index" :
        vartree = v[1]
        index = v[2]
        # try to prove that index value falls within range of array....
        if not Tables.proveSequent(C6, premises, [">=", index, ["int", "0"]]) :
            error("could not validate that array index "  \
                +  Parse.tostringExpr(index) + " is  >= 0")
        if not Tables.proveSequent(C6, premises, ["<", index, ["len", vartree]]) :
            error("could not validate that array index " \
                + Parse.tostringExpr(index) + " is < len(" \
                + Parse.tostringExpr(vartree) + ")")
    else :
        error("can't process LHS var" + v + ". I am lost.")
    # define  vold,  which is ["var", vartree[1]+"_old"]
    vold = Parse.makeOldVar(vartree) 

    if Parse.foundIn("call", e) :   
        # there is a function call in  e.  There should be just one, at top:
        eop = e[0]
        if eop == "call" :
            if Parse.foundIn("call", e[2]) :  # check that no calls in args
                error("sorry--nested function calls not allowed")
            else :  # just one, outer  call.  Good to go...
                funname = e[1]  # is ["var", VAR]
                arglist = e[2]  # is a list of 0+ etrees
                funinfo = Tables.getFunctionInfo(C6, funname)
                #print "ANALYZE FUN CALL: funame=", funname, "arglist=", arglist
                #print "funinfo=", funinfo
                if funinfo == () :
                    error("function " + funname[1] + "not defined")
                (params, pre, post, returnvar, globalvars) = funinfo

                modified_vars = modified_vars + tuple(globalvars) # update for later

                # now, enforce syntactic conditions for well-formed call:
                if len(arglist) != len(params) :
                    error("number of arguments does not match number of params")
              
                if Parse.foundIn(vartree, arglist) : # is lhs  v  mentioned in an arg?
                    error("cannot use " + vartree[1] + " as an arg of the function call")
                for g in globalvars :
                    if Parse.foundIn(g, arglist) : # is  g  mentioned in an arg?
                        error("cannot use global " + g[1] + " as an arg---it is updated in " + funname)

                # try to validate  [arglist/params]pre:
                mypre = Parse.substituteParallelTree(arglist, params, pre)
                pre_ok = (mypre in premises) \
                                 or (Tables.proveSequent(C6, premises, mypre))
                if not pre_ok :
                    mytextline = insertPrecode((myindent  \
                                      + formatUnprovedAssert(mypre) + EOL,), mytextline)
                """
                #try to validate all global invariants required by  funname:
                globalinvs = Tables.lookupGlobalInvariants(C6, globalvars)
                for inv in globalinvs :
                    g_ok = (inv in premises) \
                                 or (Tables.proveSequent(C6, premises, inv))
                    if not g_ok :
                        mytextline = insertPrecode((myindent  \
                                      + formatAssert(inv) + EOL,), mytextline)
                """
                #try to validate all global invariants before calling funname:
                unvalidated_asserts = ()
                for fassert in C6["brokeninvs"] :
                    ok = (fassert in premises) or (Tables.proveSequent(C6, premises, fassert))
                    if not ok :
                        unvalidated_asserts = unvalidated_asserts + (fassert,)

                writeTextList(indent, formatUnprovedAsserts(unvalidated_asserts))

                # define all ``old vars'' that might appear
                # in the proof steps that immediately follow this fcn call:
                ginvars = [Parse.makeInVar(g) for g in globalvars]
                goldvars = [Parse.makeOldVar(g) for g in globalvars]
                old_vars = [vold] + goldvars

                # these two vars are used at the end for proof checking:
                assign_assert = Parse.substituteParallelTree \
                                 ([v] + arglist + goldvars,  [returnvar] + params + ginvars,  post)
                #assign_assert = Parse.substituteParallelTree \
                #                ([v] + arglist,  [returnvar] + params,  post)

                newpremises = ()
                for p in premises :       # Next, revise premises:
                    newpremises = newpremises  \
                                + ( Parse.substituteParallelTree \
                                   (goldvars+[vold], globalvars+[vartree], p),)
                    #newpremises = newpremises  \
                    #            + ( Parse.substituteParallelTree \
                    #                ([vold], [vartree], p),)
                # finally, add  postcondition (assign_assert):
                newpremises = (assign_assert,) + newpremises  

                # Since the function call does not compute a value that
                # we can store, the best we can do is reset C6 to reflect
                # that  v  and  the  globalvars have changed in value:
                for x in globalvars + [v] :
                    Tables.insertAlias(C6, Parse.makeOldVar(x), x)
                Tables.reset(C6, globalvars + [v])

        else : # just one call, but it's embedded within an expression...
            error("sorry--embedded function calls not allowed")

    else :  # ordinary assignment,  x = e
        # v  turns into  v_old in assignment's  rhs  and all asserts in  C6
        Tables.insertAssign(C6, v, e) 
        vold_for_v_in_e = Parse.substituteTree(vold, vartree, optree[2])
        old_vars = [vold]
        assign_assert = ["==", v, vold_for_v_in_e]
        newpremises = (assign_assert,) + substituteTreeTuple(vold, vartree, premises)

    # If the target, v, of the assignment is an array reference, we
    # have more premises to generate:
    if v[0] == "index" :
        # vartree = v[1]   # set earlier
        # index = v[2]  # set earlier
        # vold = ["var", vartree[1]+"_old"]  # set earlier

        len_same_premise = ["==", ["len", vartree], ["len", vold]] 
        others_same_premise = \
         [ "forall", ["int", "0"], ["var", "_i"], ["len", vartree], \
              ["or", ["==", ["var", "_i"], index], \
                     ["==", ["index", vold, ["var", "_i"]], \
                            ["index", vartree, ["var", "_i"]]]] ]

        # look at the premises you collect and see if any can be revised
        #  by removing the  vold  references and reinserting  vtree:
        forallpremises = ()
        for p in newpremises :
            if p[0] == "forall" :  # ["forall", lo, i, hi, btree]
                lo = p[1]
                hi = p[3]
                #if hi == index :
                if Tables.proveSequent(C6, newpremises, ["==", hi, index]) :
                    # can retain the original: ["forall", lo, i, hi, btree]
                    #newp = Parse.substituteIndex(vartree, vold, p)
                    newp = Parse.substituteTree(vartree, vold, p)
                    forallpremises = forallpremises + (newp,)
                #if lo == index :
                if Tables.proveSequent(C6, newpremises, ["==", lo, index]) :
                    # can build ["forall", lo+1, i, hi, btree] :
                    pp = ["forall", ["+", lo, ["int","1"]], p[2], hi, p[4]]
                    #newp = Parse.substituteIndex(vartree, vold, pp)
                    newp = Parse.substituteTree(vartree, vold, pp)
                    forallpremises = forallpremises + (newp,)

        newpremises = newpremises + (len_same_premise, others_same_premise) \
                       + forallpremises

    """
    ####PULL AND MAKE INTO FUNCTION
    #### See if next line is a proof that builds on the assignment.
    # We must do this here, since the proof might have an unverified ASSERT
    # that refers to  vold (or a previous value of a global var that was
    # modified by a function call),  which means that ``precode'',  vold = v,
    # must be emitted before we emit  v = e,  the current textline. 
    
    getNextLine()
    if tokens[0] == ''''{' and myindent == indent :   # an attached proof ?
        (newest_premises, unproved_asserts, annotated_proof) \
           = checkProof(C6, newpremises)

        # see which  v_old  vars remain in unproved asserts:
        unproved_vars = filter(lambda vold: foundInTuple(vold, unproved_asserts), old_vars)

        # make list of assignments for the unproved properties of the old_vars:
        uvnames = list(set([ uv[1] for uv in unproved_vars ]))
        assignpairs = [ (uv, uv[:len(uv)-4]) for uv in uvnames ] # (v_old, v)s
        precode = makePrecode(C6, myindent, assignpairs)
        mytextline = insertPrecode(precode, mytextline)

        getNextLine()   # checkProof does not refresh  textline,  so do it now
    else :   # no proof.  Finish up....
        #newest_premises  = (assign_assert,)  #ditch all the other  newpremises
        newest_premises = newpremises
        annotated_proof = ()
        unproved_asserts = ()

    # write everything you collected:
    writeTextLists(myindent, mytextline, unproved_asserts, annotated_proof)
    for oldvar in old_vars :
        final_premises = removeAll(oldvar, newest_premises)
    Tables.erase(C6, old_vars)  # remove all mention of  v_olds from  C6

    # display what we learned:
    if verbose :
        known = map(lambda p: "# " + Parse.tostringBexpr(p),  newest_premises)
        writeTextList(myindent, ["#PREMISES BEFORE ERASURE OF old VAR: "] + known)
    #
    ####
    """
    # See if next line is a proof that builds on the assignment.
    # We must do this here, since the proof might have an unverified ASSERT
    # that refers to  vold (or a previous value of a global var that was
    # modified by a function call),  which means that ``precode'',  vold = v,
    # must be emitted before we emit  v = e,  the current textline:


    final_premises = checkAttachedProof(C6, myindent, mytextline, old_vars, newpremises)

    return (final_premises, modified_vars)  


def checkAttachedProof(C6, myindent, mytextline, old_vars, newpremises):
    """checks a proof attached to an assignment command.
       Builds on the work of  analyzeASSIGN, which is supplied as
       args to the params, to check the attached proof and write
       appropriate output.

       params: myindent: the appropriate indent for written code
               mytextline : the text of the assignment command that
                 precedes the proof to be analyzed
               old_vars: the names of vars that were updated by the assign
               newpremises : the asserts generated by the assignment,
                 to be written with the proof.

       returns:  the final_premises that escape from the assignment
                 and the analyzed proof
    """
    getNextLine()
    if tokens[0] == '"""{' and myindent == indent :   # an attached proof ?

        (newest_premises, unproved_asserts, annotated_proof) \
           = checkProof(C6, newpremises)

        # see which  v_old  vars remain in unproved asserts:
        unproved_vars = filter(lambda vold: foundInTuple(vold, unproved_asserts), old_vars)

        # make list of assignments for the unproved properties of the old_vars:
        uvnames = list(set([ uv[1] for uv in unproved_vars ]))
        assignpairs = [ (uv, uv[:len(uv)-4]) for uv in uvnames ] # (v_old, v)s
        precode = makePrecode(C6, myindent, assignpairs)
        mytextline = insertPrecode(precode, mytextline)

        getNextLine()   # checkProof does not refresh  textline,  so do it now
    else :   # no proof.  Finish up....
        #newest_premises  = (assign_assert,)  #ditch all the other  newpremises
        newest_premises = newpremises
        annotated_proof = ()
        unproved_asserts = ()

    # write everything you collected:
    if verbose :
        known = map(lambda p: myindent + "# " + Parse.tostringBexpr(p) + EOL, \
                     newpremises)
        mytextline = mytextline \
                     + (myindent + "#PREMISES FOR ATTACHED PROOF, IF ANY: " + EOL)
        for line in known :
            mytextline =  mytextline + line

    writeTextLists(myindent, mytextline, unproved_asserts, annotated_proof)
    final_premises = newest_premises
    for oldvar in old_vars :
        final_premises = removeAll(oldvar, final_premises)
    Tables.erase(C6, old_vars)  # remove all mention of  v_olds from  C6
    
    # display what we learned:
    #if verbose :
    #    known = map(lambda p: "# " + Parse.tostringBexpr(p),  newest_premises)
    #    writeTextList(myindent, ["#PREMISES BEFORE ERASURE OF old VAR: "] + known)
    #
    ####
    return final_premises



def analyzeIF(C6, premises, optree) :
    """analyzes the current text line, an IF, of usual syntax.
       
       params:  C6: constraint tables;  premises: premise tuple of btrees;
                optree: parse of current text line: ["if", btree]

       reads subsequent then- and else- arms and analyzes both;
       updates  C6  by _removing_ all entries that refer to variables
       modified in either of two arms

       returns: finalAssertionOfProof and tuple of modified vars
    """
    myindent = indent
    writeText(textline)  # write  'if:'

    # the then- and else- arms use their own C6tables and premises:
    btest = optree[1]  
    notbtest = ["not", btest]
    thenpremises = (btest,) + premises
    elsepremises = (notbtest,) + premises

    # check btest for well-formedness:
    #OLD Tables.checkTest(C6, btest)

    thenC6 = Tables.copy(C6)
    Tables.insertRelation(thenC6, btest)

    # analyze then-arm:
    getNextLine()
    if verbose :
        # display what we learned:
        known = map(lambda p: "# " + Parse.tostringBexpr(p),  thenpremises)
        writeTextList(indent, ["#PREMISES FOR THEN-ARM: "] + known)

    (then_assert, then_modifications) = analyzeCMDSEQUENCE(thenC6, myindent, thenpremises)

    # next line should be  ELSE:
    if tokens[0] == "else" :
        (optree, extra_tokens) = Parse.parseCOMMANDLINE(tokens)
        writeText(textline)  # write 'else:'
        getNextLine()
        if verbose :
             # display what we learned:
             known = map(lambda p: "# " + Parse.tostringBexpr(p),  elsepremises)
             writeTextList(indent, ["#PREMISES FOR ELSE-ARM: "] + known)
        # analyze  else-arm:
        elseC6 = Tables.copy(C6)
        Tables.insertRelation(elseC6, notbtest)
        (else_assert, else_modifications) = analyzeCMDSEQUENCE(elseC6, myindent, elsepremises)
    else :  # oops--- programmer omitted the else arm!  Not nice, but ...
        (else_assert, else_modifications) = ((notbtest,), ())

    # Finish: make final assertions.
    # Note: both then_assert and else_assert are tuples of trees,
    # so the tuples must be formatted as conjunction optrees...
    #if_assert = ["or", Parse.conjunctionOf(then_assert),
    #                   Parse.conjunctionOf(else_assert)]
    common_asserts = ()
    for f in then_assert :
        if f in else_assert : common_asserts = common_asserts + (f,)

    thenpart = ()
    for f in then_assert :
        if f not in common_asserts : thenpart = thenpart + (f,)
    elsepart = ()
    for f in else_assert :
        if f not in common_asserts : elsepart = elsepart + (f,)
    if_assert = ["or", Parse.conjunctionOf(thenpart),
                       Parse.conjunctionOf(elsepart)]
    if if_assert[1] == ["True"] or if_assert[2] == ["True"] :
        if_assert = ["True"]
    
    # and remove all modified vars from C6:
    all_modifiedvars = ()
    for v in then_modifications + else_modifications :
        if v not in all_modifiedvars :
            all_modifiedvars = all_modifiedvars + (v,)
    Tables.reset(C6, all_modifiedvars)
    
    # do the same for the premises that exit the conditional:
    exitpremises = premises
    for v in all_modifiedvars:
        exitpremises = removeAll(v, exitpremises)

    return ((if_assert,) + common_asserts + exitpremises , all_modifiedvars)



def analyzeWHILE(C6, premises, optree) :
    """analyzes the current text line, a WHILE.  It must have form:
          while BEXPR :
              '''{ invariant BEXPRI  modifies VARLIST }'''
              BODY, a CMDSEQUENCE
       
       params:  C6: constraint tables;  premises: tuple of btrees;
                optree: parse of current text line: ["while", btree]

       Reads invariant-modifies clause and checks if invariant proved on entry;
       removes from  C6 all vars in VARLIST (they are _not_ invariant!)
       Analyzes loop body; finishes by checking if invariant holds and
       by updating  C6  by _removing_ all entries in VARLIST

       returns:  (not btree and invariant)  and tuple of modified vars
    """
    myindent = indent
    mytextline = textline  # holds the source text for  'while B :'

    btest = optree[1]
    notbtest = ["not", btest]

    # check btest for well-formedness:
    #OLD Tables.checkTest(C6, btest)

    # Read invariant-modifies-clauses:
    # NOTE: modifies holds list of all vars that are altered in loop body
    #  invariant is loop invariant assertion, a btree
    #  asserttext is tuple of textlines read by  checkInvariantModifies
    getNextLine()
    if tokens[0] == '"""{' :
        (log, textread) = checkModifier()
        if ("invariant" not in log) or ("modifies" not in log) :
            error("loop should begin with invariant+modifies clauses")
        invariant = log["invariant"]
        modifies = log["modifies"]
    else :
        print "WARNING: loop should have an invariant+modifies clause"
        invariant = ["True"]  # no invariant; nothing to prove  )-:
        modifies = []  # I dunno which vars are modified.  Will patch later
        textread = ()  # no text consumed by missing clause

    invariant_ok = (invariant in premises) or (Tables.proveSequent(C6, premises, invariant))
    if not invariant_ok : # user didn't prove the invariant on entry?
        precode = formatUnprovedAssert(invariant)
        mytextline = insertPrecode((myindent + precode + EOL,), mytextline)
    writeTextLists(myindent, mytextline, (), textread)

    # clean up C6 by resetting all vars that will be modified in loop body:
    Tables.reset(C6, modifies)

    # do the same for the premises that can enter the loop body:
    bodypremises = premises
    for v in modifies :
        bodypremises = removeAll(v, bodypremises)
    exitpremises = bodypremises   # save invariant premises for exit....

    bodypremises = (btest, invariant) + bodypremises
    bodyC6 = Tables.copy(C6)
    Tables.insertRelation(bodyC6, btest)
    Tables.insertRelation(bodyC6, invariant)


    # analyze loop body
    if verbose :
        # display what we learned:
        known = map(lambda p: "# " + Parse.tostringBexpr(p),  bodypremises)
        writeTextList(indent, ["#PREMISES FOR LOOP BODY: "] + known)

    bodyindent = indent  # remember how loop body is indented
    (body_asserts, body_modifications) = analyzeCMDSEQUENCE(bodyC6, myindent, bodypremises)


    # Finish: see if  body_asserts  includes  invariant; if not, insert ASSERT
    invariant_ok = (invariant in body_asserts) or (Tables.proveSequent(C6, body_asserts, invariant))
    if not(invariant_ok) :
        writeTextList(bodyindent, (formatUnprovedAssert(invariant),))

    # check if list of modified vars matches what happened in the body:
    if modifies != [] :
        ok = varSublistOf(body_modifications, modifies)
        if not(ok) :
            error("these vars were modified in the loop: " + Parse.tostringVarlist(body_modifications))
            Tables.reset(C6, body_modifications)
    else :  # user didn't say what was modified, so patch C6 here:
        Tables.reset(C6, body_modifications)

    # Revise C6 tables at loop exit:
    Tables.insertRelation(C6, notbtest)
    Tables.insertRelation(C6, invariant)
    return ((invariant, notbtest) + exitpremises,  body_modifications)


def analyzeDEF(C6, premises, optree) :
    """analyzes a function definition, starting with the current line,
       which is the header line.   Requires this format:
          def f(params):
          '''{ pre BEXPR1  post BEXPR2 [ return VAR ] }'''  (all optional)
          [globals VARLIS ]  (optional)
          BODY, a CMDSEQUENCE   # cannot assign to any of  params
          return VAR

      If  function_asserts  mode on,  will generate an  ASSERT BEXPR1   command
      Will take these actions:
      ---save function definition plus, pre, post, globals in existing C6 table
      ---generates a new C6 for analyzing fcn body and inserts pre and
         all relevant globalinvs and all brokeninvs  into it
      --- generates assigns,  g_in = g,  for globals,  g_in,  in BEXPR2
      ---analyzes its BODY with new C6
      ---afterwards, checks that  no param was modified; all brokeninvs
          now hold; postcondition holds; 
     
       returns: BEXPR2  and   function name as only modified var
    """

    breakpt("Entering analyzeDEF", C6, [("optree=", optree)])

    global textline  # possible will append some text to the textline...

    myindent = indent
    myglobalvars = []      # the vars declared global by this function

    funname = optree[1]
    params = optree[2]
    writeText(textline)
    # verify that all params are disjoint names:
    for i in range(len(params)):
        if params[i] in params[i+1:] :
            error("all parameter names must be distinct")

    getNextLine()
    # Read pre-post-clauses:
    if tokens[0] == '"""{' :
        (log, textprocessed) = checkModifier()
        for line in textprocessed :
            writeText(line)
        if "pre" not in log :
            preassert = ["True"]
            print "WARNING: function should begin with pre/post/return assertions"
        else :
            preassert = log["pre"]
        if "post" not in log :
            postassert = ["True"]
            print "WARNING: function should begin with pre/post/return assertions"
        else :
            postassert = log["post"]
        #if ("pre" not in log) or ("post" not in log)  :
        #    error("function must begin with pre/post/return assertions")
        #preassert = log["pre"]
        #postassert = log["post"]
        if "return" in log :
            returnvar = log["return"]
        else :
            returnvar = ["_none"]
    else :  # no pre-post-answer  )-:
        print "WARNING: function should begin with pre/post/return assertions"
        preassert = ["True"]
        postassert = ["True"]
        returnvar = ["__none"]


    # see if globals line present:
    if tokens[0] == "global" :
        (gtree, extra_tokens) = Parse.parseCOMMANDLINE(tokens)
        myglobalvars = gtree[1]
        # these invariants will get clobbered by the function's body:
        brokeninvariants = Tables.lookupGlobalInvariants(C6, myglobalvars)

        # See if any globals, g, are mentioned as  g_in  in postassert:
        ginvars = [Parse.makeInVar(g) for g in myglobalvars ]
        gpostinvars = [g for g in ginvars  if Parse.foundIn(g, postassert)]

        # Generate assignments,  g_in = g,  and adjoin to textline:
        gnames = list(set([ g[1] for g  in gpostinvars ]))
        gpairs = [ (g, g[:len(g)-3]) for g in gnames ] # (g_in, g)s
        precode = makePrecode(C6, indent, gpairs)
        for line in precode:
           textline = textline + line
        writeText(textline)
        getNextLine()

        """
        # generate premises of form,  g_in == g :
        # FOR ARRAYS??:  forall 0 <= i < len(g), g_in[i] == g[i]  MAYBE NOT????
        gin_premises = []
        for gin in gnames :
            if gin in garraynames???! :
                gin_premises.append(["forall", 0?, _i, len(gin)?, g[_i]=gin[_i]]) # FIXME
            else :
                gin_premises.append(["==", Parse.makeVar(gin), Parse.makeVar(gin[:len(g)-3])])
        """
    else :
        myglobalvars = []
        brokeninvariants = []
        """
        gin_premises = []
        """
        #ginvars = []   # needed below, when initializing  bodyC6  for fcn body
        gpostinvars = []

    # save the function definition:
    Tables.insertFunction(C6, funname, params, preassert, postassert, returnvar, myglobalvars) 

    # Make a new C6 table for processing the function's body:
    # First, extract from   brokeninvariants + pre + post + gin_premises
    #  all (scalar) and array variable references
    # Next, add all param names to scalars.   Subtract the two lists
    #  to determine the vars that should be present in the store that
    #  enters the function's body:
    my_vars = params + myglobalvars

    # determine which of  my_vars  are arrays:
    my_arrays = []
    for avar in myglobalvars:
        if Tables.lookupType(C6, avar[1]) == "array" :
            my_arrays.append(avar)

    for assertion in brokeninvariants + [preassert, postassert] :
        my_arrays = my_arrays + [ vtree for vtree in my_vars
                                  if Parse.foundArrayRef(vtree, assertion) ]
    my_arrays = Parse.removeDuplicates(my_arrays)

    my_scalars = Parse.removeDuplicates(Parse.subtractVars(my_vars, my_arrays))

    bodyC6 = Tables.copyWithoutStore(C6, funname, my_scalars, my_arrays, myglobalvars, brokeninvariants)  

    # for all the  g_in vars,
    #   generate premises of form,  g_in == g ,  for simple vars;
    #   for arrays, generate,  forall 0 <= i < len(g), g_in[i] == g[i]

    gin_premises = []
    for gin in gpostinvars:  # look at each  ["var","g_in"]:
        g = Parse.makeVar(gin[1][:len(gin[1])-3])  # build  ["var","g"] )-:
        if g in my_arrays:
            iindex = ["var", "_i"]
            gin_premises.append( \
                ["forall", ["int","0"], iindex, ["len", g], \
                  ["==", ["index", g, iindex], ["index", gin, iindex]]])
            gin_premises.append( ["==", ["len", g], ["len", gin]] )
        else :
            gin_premises.append(["==", g, gin])

    # if any global  g  is referenced as  g_in  in postassert,
    # then store assignment,  g_in = g,  in  bodyC6:
    for g in gpostinvars:
        ginname = g[1] # "g_in"
        gname = ginname[:len(ginname)-3]  # "g"
        Tables.insertAlias(bodyC6, g, ["var",gname] )

    # now, we save the preassert and global invariants:
    for inv in [preassert] + brokeninvariants + gin_premises :
        Tables.insertRelation(bodyC6, inv) 

    if function_asserts :  # generate ASSERTS for function body?
        writeTextList(indent, formatAsserts(myinvariants + (preassert,)))

    breakpt("READY TO ANALYZE FCN BODY with", bodyC6, [])

    # Now process body: 
    bodyindent = indent  # remember how much body is indented
    bodypremises = (preassert,) + tuple(brokeninvariants + gin_premises)

    if verbose : 
        known = map(lambda p: "# " + Parse.tostringBexpr(p), bodypremises)
        writeTextList(bodyindent, ["#PREMISES FOR NEXT LINE: "] + known)

    (body_asserts, body_modifications)  \
        = analyzeCMDSEQUENCE(bodyC6, myindent, bodypremises)

    # Finish up:
    for p in params :
        for vtree in body_modifications :
            if (vtree[0] == "var" and vtree[1] == p[1])  or \
               (vtree[0] == "index" and vtree[1][1] == p[1] ) :
                error("sorry: cannot assign to input parameter " + p[1])
                break

    breakpt("READY TO CHECK POSTASSERT with", bodyC6, [])

    # see if  body_assert  implies  postassert and all global invarants:
    unvalidated_asserts = ()
    for fassert in brokeninvariants + [postassert] :
        ok = (fassert in body_asserts) or (Tables.proveSequent(bodyC6, body_asserts, fassert))
        if not ok :  unvalidated_asserts = unvalidated_asserts + (fassert,)

    writeTextList(bodyindent, formatUnprovedAsserts(unvalidated_asserts))

    funvar =  Parse.makeVar(funname)
    Tables.erase(C6, [funvar])  # if  funname  used earlier, erase it;
                                  # it's now a function
    new_premises = removeAll([funvar], premises)  # remove all mention
                                  # of  funname  from original incoming premises
    return (new_premises, (funvar,))  # the function's pre-post don't leave
                                       # till the function is called...
    # FIXME: augment first tuple to assert that  callable(funname)  too.



def analyzeRETURN(C6, premises, optree) :
    """analyzes the current text line, a  RETURN  command
        
       params:  C6: constraint tables;  premises: premise tuple of btrees;
                optree: parse of current text line: ["assert", btree]
    
       Checks that premises at the point of function return satisfy
       postcondition and all broken global invariants.  Checks that
       value (if any) returned is consistent with info in function's
       ``returns VAR'' header line.
       returns: premises and empty tuple of updated vars
    """
    # look up postcondition, global invariants, and returned-answer var
    # and validate them now:
    (postassert, ansvar, brokeninvs) = Tables.getLocalReturnInfo(C6)

    unvalidated_asserts = ()
    for fassert in brokeninvs + [postassert] :
        ok = (fassert in premises) or (Tables.proveSequent(C6, premises, fassert))
        if not ok : 
            unvalidated_asserts = unvalidated_asserts + (fassert,)
    writeTextList(indent, formatUnprovedAsserts(unvalidated_asserts))

    if len(optree) > 1 :
        returnval = optree[1]
        if returnval != ansvar  and  ansvar != ["__none"] :
           error("sorry -- you must use the specified return variable in the header")
    elif ansvar[0] != "_none" :
           error("you must return a var that matches the one in the header")

    writeText(textline)
    getNextLine()

    return (premises + (postassert,), ())


def analyzeAPPEND(C6, premises, optree) :
    """analyzes the current text line, a  varname.append(expr)  command
        
       params:  C6: constraint tables;  premises: premise tuple of btrees;
                optree: ["append", lhstree, etree]
    
       returns: premises and tuple of updated vars
    """
    breakpt("entered analyzeAPPEND", C6, ())

    myindent = indent
    mytextline = textline

    v = optree[1]
    vold = Parse.makeOldVar(v)
    # verify that a listname is used with append:
    if v[0] != "var" :
        error("append can be used only with an array/list name")

    e = optree[2]
    lenv = ["len", v]
    lastindex = ["-", lenv, ["int", "1"]]

    assignassert = ["==", ["index", v, lastindex], e]
    lenassert = ["==", lenv, ["+", ["len", vold], ["int", "1"]]]
    revised_premises = \
        tuple([ Parse.substituteIndex(v, vold, Parse.substituteTree(vold, v, p)) \
                for p in premises ])  
    newpremises = (assignassert, lenassert) + revised_premises


    #Tables.insertAssign(C6, ["index", v, lastindex],  e)
    #Tables.incrementLen(C6, v, 1)
    Tables.insertAppend(C6, v, e)

    breakpt("APPEND: ready to check proof", C6, [("newpremises", newpremises)])

    #writeText(textline)
    #getNextLine()
    old_vars = [vold]

    """
    ####PULL AND MAKE INTO FUNCTION
    #### See if next line is a proof that builds on the assignment.
    # We must do this here, since the proof might have an unverified ASSERT
    # that refers to  vold (or a previous value of a global var that was
    # modified by a function call),  which means that ``precode'',  vold = v,
    # must be emitted before we emit  v = e,  the current textline. 
   
    getNextLine()
    if tokens[0] == ''''{' and myindent == indent :   # an attached proof ?
        (new_facts, unproved_asserts, annotated_proof) \
           = checkProof(C6, newpremises)
        newest_premises = new_facts

        # see which  v_old  vars remain in unproved asserts:
        unproved_vars = filter(lambda vold: foundInTuple(vold, unproved_asserts), old_vars)

        # make list of assignments for the unproved properties of the old_vars:
        uvnames = list(set([ uv[1] for uv in unproved_vars ])) 
        assignpairs = [ (uv, uv[:len(uv)-4]) for uv in uvnames ] # (v_old, v)s
        precode = makePrecode(C6, myindent, assignpairs)
        mytextline = insertPrecode(precode, mytextline)

        getNextLine()   # checkProof does not refresh  textline,  so do it now
    else :   # no proof.  Finish up....
        #newest_premises  = (assign_assert,)  #ditch all the other  newpremises
        newest_premises = newpremises
        annotated_proof = ()
        unproved_asserts = ()

    # display what we learned:
    if verbose :
        known = map(lambda p: "# " + Parse.tostringBexpr(p),  newest_premises)
        writeTextList(myindent, ["#PREMISES BEFORE ERASURE OF old VAR: "] + known)
    # write everything you collected:
    writeTextLists(indent, mytextline, unproved_asserts, annotated_proof)
    for oldvar in old_vars :
        final_premises = removeAll(oldvar, newest_premises)
    Tables.erase(C6, old_vars)  # remove all mention of  v_olds from  C6
    #
    ####
    """

    final_premises = checkAttachedProof(C6, myindent, mytextline, old_vars, newpremises)
    return (final_premises, (["index", v, lastindex],))


def analyzeCMDSEQUENCE(C6, exitindent, premises) :
    """analyzes a sequence of commands, starting with the one awaiting
       in the current value  of  textline,indent,tokens
       If the sequence is
       Terminates the analysis when a new  textline  is encountered whose indent
       is less than where it was when the sequence started
       _or_  when  textline == ""  (EOF)
       
       params:  C6: constraint tables; 
                exitindent: the indentation level where we should exit
                premises: premise tuple of btrees;

       passes updates to  C6  to each command in sequence

       returns: finalAssertions and tuple of all modified vars in the sequence
    """
    myindent = indent
    previousline_indent = indent
    modified_vars = ()
    nextpremises = premises 
    while indent > exitindent  and  tokens != (EOF,) :
        if previousline_indent != indent :
            error("uneven indentation of commands")
        previousline_indent = indent
        if tokens[0] == '"""{' :
            (newpremises, unprovedasserts, annotatedproof) \
                = checkProof(C6, nextpremises)
            writeTextLists(myindent, "", unprovedasserts, annotatedproof)
            breakpt("finished proof:", C6, [])
            getNextLine()  # checkProof  does not refresh  tokens;  do it now
        else :
            (optree, extra_tokens) = Parse.parseCOMMANDLINE(tokens)
            op = optree[0]
            if op == "=" :
                f = analyzeASSIGN
            elif  op == "assert" :
                f = analyzeASSERT
            elif op == "if" :
                f = analyzeIF
            elif op in ("pass", "print", "raw_input"):
                f = analyzePASS
            elif op == "while" :
                f = analyzeWHILE
            elif op == "def" :
                f = analyzeDEF
            elif op == "return" :
                f = analyzeRETURN
            elif op == "append" :
                f = analyzeAPPEND
            elif op in ("else", "global") :
                error("unexpected " + op)
                break   # quit loop and hope caller function can recover
            else :
                f = (lambda x,y,z: ((),()) )
                error("I can't decode this command:")
                writeText(textline)
                getNextLine()

            (newpremises, more_mod_vars) = f(C6, nextpremises, optree)
            modified_vars = modified_vars + more_mod_vars
            breakpt("finished command:", C6, [("optree=",  optree)])

        # remove duplicates from newpremises to make nextpremise set:
        nextpremises = ()
        for p in newpremises :
            if p not in nextpremises and p != ["True"] : 
                nextpremises = nextpremises + (p,)

        if verbose : 
            known = map(lambda p: "# " + Parse.tostringBexpr(p), nextpremises)
            writeTextList(previousline_indent, ["#PREMISES FOR NEXT LINE: "] + known)


    return (nextpremises, modified_vars)


########################################################################

"""routine searching and substitution functions for operator trees
   and tuples of trees
"""

def substituteTreeTuple(replacement, pattern, tuple):
    """performs substitution on all trees within the  tuple"""
    #return map(lambda tree: Parse.substituteTree(replacement, pattern, tree), tuple)
    ans = ()
    for tree in tuple :
        ans = ans + (Parse.substituteTree(replacement, pattern, tree),)
    return ans


def foundInTuple(pattern, tuple):
    """searches for an occurrence of pattern within _any_ tree in the tuple"""
    for tree in tuple :
        if Parse.foundIn(pattern, tree) :
            return True
    return False  # because no earlier success

def removeAll(pattern, tuple) :
    """removes every tree in the sequence that contain an instance
       of  pattern.  Returns a new, reduced tuple
    """
    ans = ()
    for tree in tuple :
        if not Parse.foundIn(pattern, tree) :
            ans = ans + (tree,)
    return ans


def varSublistOf(subl, mainl):
    """calculates if every var in sequence subl  is also in  mainl

       params: subl - a sequence of ["var", v] and ["index" ["var", v], _] trees
               mainl - a sequence of ["var", v] trees
    """
    ans = True
    for item in subl :
        if item[0] == "var" :
            v = item
        elif item[0] == "index" :
            v = item[1]
        else :
            v = []
            error("varSublistOf can't figure out the list of mod vars")
        ans = ans and (v in mainl)
    return ans



########################################################################

"""Here are the functions that parse/analyze Hoare-logic proofs:"""


def checkProof(C6, premises) :
    """commencing with the current textline and tokens,
       checkProof reads and attempts to validate the assertions
       in a multiline logic proof.

     params:  C6: constraint tables;  premises: premise tuple of btrees
     updates  C6  with new knowledge gained from the proof

     returns: a triple:

       (finalAssertOfProof: the last asserts, a tuple of btrees, in the proof

        unprovedAsserts: a tuple of btrees of all the bool exprs within
                         the proof lines that _weren't_ validated. 
                         Will later be embedded in the program as
                         ASSERT commands

        annotatedProof: a tuple of text lines of the entire proof that was
                        processed.  Will be copied back into the program
      )

      NOTE that this function _does not_ reset  textline and tokens  to a fresh
      source line on exit!  This is because its caller may wish to emit
      ``precode'' and the annotated proof to the output file before the
      next source line is read.   )-:
    """

    global tokens, textline
    proof = {}   # the parsed lines of the proof so far; each entry has form,
                 #   proof[linenum] = (bfact, justification)
    annotated_proof = ()  # the (annotated) lines of the proof so far
    unproved_asserts = () # the btrees from proof lines that I couldn't validate
    bgoal = ()   # holds the assert(s) justified on the current proof line 


    def getFact(linenum):
        """helper function that looks up the fact at proof line  linenum"""
        if linenum in proof :  # valid line number reference?
           bfact = proof[linenum][0]
        else :
           error("invalid line number: " + textline)
           bfact = []
        return bfact


    # START:
    if tokens[0] == '"""{' :
        tokens = tokens[1:]   # ditch the """{
    if len(tokens) == 0 :
        annotated_proof = annotated_proof + (textline,)
        getNextLine()

    finished = False
    # invariant: each iteration, loop works with a fresh textline
    while not finished and  textline != "" :
       if  tokens[0] != '}"""' :
           # process the proof line:
           (ptree, rest) = Parse.parsePROOFLINE(tokens)
           success = False  # remembers whether we validate this line's assert
           # save parsed proof line:
           if ptree[0].isdigit() :   # proof line has form,  [num, btree, just]
               (num, bgoal, just) = ptree
               if num in proof :
                   error("line already exists with this number: " + textline)
               proof[num] = (bgoal, just) 
               # cases on form of justification:
               op = just[0]
               if op == "premise" :
                   success = bgoal in premises
               elif op == "copy" :
                   bfact = getFact(just[1])
                   success = (bgoal == bfact) and (num != just[1]) # self-reference disallowed
               elif op == "globalinv" :
                   success = (bgoal in C6["globalinvs"]) # or \
                             #Tables.proveSequent(C6, C6["globalinvs"], bgoal)
               elif op == "def" :
                   success = Tables.matchDef(C6, bgoal)
               elif op == "subst" :
                   eqn = getFact(just[1])
                   bfact = getFact(just[2])
                   success = False
                   if eqn[0] == "==" :
                       pattern = eqn[1]
                       replacement = eqn[2]
                       success = \
                       (num != just[1] and num != just[2]) \
                       and \
                       ((Parse.substituteTree(pattern, replacement, bgoal)      \
                         == Parse.substituteTree(pattern, replacement, bfact)) \
                       or \
                       (Parse.substituteTree(replacement, pattern, bgoal)      \
                         == Parse.substituteTree(replacement, pattern, bfact)))
               elif op == "algebra" :
                   bfacts = ()
                   #for index in range(1,len(just)):
                   #    bfacts = bfacts + (getFact(just[index]),)
                   for index in range(1,len(just)):
                       justnum = just[index]
                       if num != justnum :  # not a circular justification ?
                           bfacts = bfacts + (getFact(just[index]),)
                       else :
                           print "WARNING: circular justification of proof line ignored"
                   if bfacts == () :
                       print "WARNING: must list some premises to do algebra"
                       success = False
                       #success = Tables.proveSequent(C6, bfacts, bgoal)
                   else :
                       success = Tables.proveSequent(C6, bfacts, bgoal)
               elif op == "ande" :
                   bfact = getFact(just[1])
                   if bfact[0] == "and" :
                       success = (bgoal == bfact[1] or bgoal == bfact[2])
               elif op == "ori" :
                   bfact = getFact(just[1])
                   if bgoal[0] == "or" :
                       success = (bgoal[1] == bfact or bgoal[2] == bfact)
               elif op == "ore" :
                   bfact = getFact(just[1])
                   if bfact[0] == "or" :
                       success = (bfact[1] == bgoal and bfact[2] == bgoal) \
                                 or (Tables.proveSequent(C6, (bfact[1],), bgoal) \
                                     and Tables.proveSequent(C6, (bfact[2],), bgoal))
               elif op == "andi" :
                   bfact1 = getFact(just[1])
                   bfact2 = getFact(just[2])
                   if bgoal[0] == "and" :
                       success = (bfact1 == bgoal[1] and bfact2 == bgoal[2])
               elif op == "foralli" :  # bgoal = ["forall" lo, i, hi, btree]
                   # collect facts that will use to prove bgoal:
                   bfacts = ()
                   for index in range(1,len(just)):
                       bfacts = bfacts + (getFact(just[index]),)
                   success = Tables.proveUniversal(C6, bfacts, bgoal)
               elif op == "foralle" : 
                   # collect facts that will use to prove bgoal:
                   bfacts = ()
                   for index in range(2,len(just)):
                       bfacts = bfacts + (getFact(just[index]),)
                   index = just[1]    # index used to elim forall
                   # Next, find the forall-claim that we eliminate:
                   foralls = [ f for f in bfacts if f[0] == "forall"]
                   success = False
                   # to prove,  bfact[0] must be   ["forall" lo, i, hi, btree]
                   # so that we can prove that  index >= lo  and  index < hi  
                   # and we can match   [index/i]btree == bgoal :
                   for f in foralls :
                       stree = Parse.substituteTree(index, f[2], f[4])
                       if stree == bgoal \
                          and  Tables.proveSequent(C6, bfacts, [">=", index, f[1]]) \
                          and  Tables.proveSequent(C6, bfacts, ["<", index, f[3]]) :
                           success = True
                           break
               elif op == "substindex" :
                   bfact = getFact(just[1])
                   if bgoal[0] == "forall" and bfact[0] == "forall" :
                       factindex = bfact[2]
                       goalindex = bgoal[2]
                       success =  (bgoal \
                           == Parse.substituteTree(goalindex, factindex, bfact))
               else :
                   error("bad justification for proofline " + num)

           elif ptree[0] == "globalinv" :   # ["globalinv", bgoal]
               bgoal = ptree[1]
               success = (bgoal in premises) or (Tables.proveSequent(C6, premises, bgoal))
               Tables.insertGlobalInvariant(C6, bgoal)
           elif ptree[0] == "def" : # ["def", btreeassert]
               Tables.insertDef(C6, ptree[1])
               success = True
           elif ptree[0] == "return" :  # copy and return multiple facts
               bgoal = tuple([getFact(num) for num in ptree[1:]])
               success = True
           else : # bah --- user entered an  invariant or modifies clause )-:
               error("sorry--a numbered proof cannot include other modifiers")

           if success :
               judgement = "OK"
           else :
               judgement = "??"
               unproved_asserts = unproved_asserts + (bgoal,)

           #annotate the current proof textline with the judgement:
           index = textline.find(".")
           if index != -1 :
               textline = textline[:index + 1] + judgement + textline[index+1:]
           else :
               index = textline.find("globalinv")
               if index != -1 :
                   textline = textline[:index + 9] + judgement + textline[index+9:]
               else :
                   index = textline.find("def")
                   if index != -1 :
                       textline = textline[:index + 3] + judgement + textline[index+3:]
                   else : textline = judgement + textline

       annotated_proof = annotated_proof + (textline,) 
       if '}"""' in tokens :  # is this the last line of the proof?
           finished = True
       else :
           getNextLine()

    # if bgoal is a single btree, place it into a singleton:
    if not(isinstance(bgoal, tuple)) :  bgoal = (bgoal,)

    if all_asserts :  # should we include incoming premises in our answer ?
        conclusions = bgoal + premises
    else :
        conclusions = bgoal

    return (conclusions, unproved_asserts, annotated_proof)


def checkModifier():
    """reads proof documentation of this form:
       '''{ [keyword MODIFIER]* }'''
       where  keyword in ("invariant", "modifies", "pre", "post")
              MODIFIER is  btree or varlist

       returns a pair: a dictionary that maps each keyword to its modifier
                       a tuple holding the source textlines read
       Also, will set textline and tokens to the next line to be analyzed.
    """
    global tokens, textline
         
    keywords = ("invariant", "modifies", "pre", "post", "return")
    text = (textline,)  # text read
    ans = {}

    if tokens[0] == '"""{' :
        tokens = tokens[1:]   # discard for parse:
    if len(tokens) == 0 :
        getNextLine()
        text = text + (textline,)
    while tokens[0] != '}"""' :
        (ptree, rest)  = Parse.parsePROOFLINE(tokens)
        op = ptree[0]
        if op in keywords :
            ans[ptree[0]] = ptree[1]   # save keyword and value
        else :
            error("invariant/modifies  or  pre/post  required here")
        if rest[0] == EOL :
             getNextLine()
             text = text + (textline,)
        else :
             tokens = rest
    getNextLine()   # discard the }'''
    return (ans, text)



###########################################################################

def error(message):
    global assert_errors
    m = "# ERROR: " + message + EOL
    writeText(m)
    print m,
    print
    assert_errors = True
    

def breakpt(message, C6, arglist) :
    if debug :
        print
        print "BREAKPT: ", message
        print "current C6=",  C6
        print
        print "store=", C6["store"]
        print
        print "heap=", C6["heap"]
        print
        print "rels=", C6["rels"]
        for arg in arglist :
            print
            print arg[0], arg[1]
        print
        raw_input("Press Enter to continue")
        print

def adjoinHeader():
    """generates header code for annotated programs"""
    header = \
"""
#####HEADER#################################################################

def readInt(message = "Type an int: ") :
    #readInt  requests and reads an int typed by a user from the display.
    #  param: message - a string, the input prompt; default is 'Type an int:'
    #  returns the input int.  (Will repeat the request till user types an int.)
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
    #forall  computes the truth value of  (FORALL low <= i < high, expr).
    # In Python, this must be coded as  forall(low, high, lambda i: expr).
    #  params: low, high - ints;  quant_expr - a function expression. 
    #  returns : True iff  expr_i  is True for all i in range(low,high)
    outcomes = [ quantified_expr(i)  for i in range(low, high) ]
    return  not(False in outcomes)

##########################################################################

"""
    if function_asserts : writeText(header)
    # end adjoinHeader function!    



###########################################################################
##########################################################################

### START-UP CODE 


def main(filename, options = "") :
    """main driver for analyzer.  start here to do everything"""
    global verbose, debug, function_asserts, all_asserts, assert_errors, textline

    import sys
    ok = True  # did execution complete ok ?
    resetGlobals()

    if "v" in options :
        verbose = True     # embeds automatically generated asserts
        Tables.setVerbose()
    if "x" in options :
        function_asserts = True # embeds header code and function asserts
    if "d" in options :
        debug = True     # activates any  breakpt  calls in this program
        Tables.setDebug()
    if "a" in options :
        all_asserts = True # makes proof segments return premises + goal

    # use this when you want debug info from execution errors:
    if debug :
        Scan.init(filename)
        adjoinHeader()
        C6 = Tables.empty()
        premises = ()
        getNextLine()

        analyzeCMDSEQUENCE(C6, -1, premises)      # note: -1 means no prior indent
        if textline != "" : writeText(textline)   # the very last source line...
        print
        if assert_errors :
            print "Only partial success; please see output file."
        else :
            print "All assertions verified.  (-:"
    else : # not debug
        #naive users use this:
        try:
            Scan.init(filename)
            adjoinHeader()
            C6 = Tables.empty()
            premises = ()
            getNextLine()

            analyzeCMDSEQUENCE(C6, -1, premises)
            if textline != "" : writeText(textline)
            print
            if assert_errors :
                print "Only partial success; please see output file."
            else :
                print "All assertions verified.  (-:"
        except:
            print
            print "Due to internal error,  Analyze.py  must terminate.  Sorry."
            print
            print "Please verify that the filename (and its path) are correct,"
            print "and if so, please inspect your program for syntax errors."
            print
            print str(sys.exc_info())
            ok = False
            raw_input("Press Enter to terminate")

    Scan.quit()

    return ok

