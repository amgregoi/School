"""CNF  maps a parse tree of a bexpr into its conjunctive-normal form.
"""

import Scan
import Parse  # for access to tree formats, tokens, functions

######################################################################
""" test driver:"""

def main(filename) :
    global tokentuple
    Scan.init(filename)
    while True :
       raw_input("Press Enter")
       print
       (textline, indent, tokens) = Scan.readLine()
       tree, rest = Parse.parseCOMMANDLINE(tokens)
       print "tree =", tree
       print "what's left over:", rest
       prop2 = nnfOf(tree[1])
       print "- shifted inwards:"
       print prop2
       print
       prop3 = nfOf("or", "and", prop2)
       print "cnf:"
       print  prop3
       print
       prop4 = flatten("or", "and", prop3)
       print "flattened cnf:"
       print  prop4
       print
       prop5 = removeDuplicates(prop4)
       print "no duplicates:", prop5
       prop6 = removeOpposites(prop5)
       print "simplified cnf:"
       print prop6
       for clause in prop6 :
           print clause
    Scan.quit()
#################################################################

def cnf(btree): return nf("and", "or", btree)

def dnf(btree): return nf("or", "and", btree)

def nf(outerop, innerop, btree) :
    """nf maps  btree  into a flattened, simplified list in the
       normal form defined by  outerop  and  innerop"""
    #if btree[0] == "forall" :
    #    error("Cannot normalize a forall assertion.  Sorry")
    #    answer = []  # sorry, won't try to format a universal...
    #else :
    nf1 = nfOf(outerop, innerop, nnfOf(btree))
    answer =  removeOpposites(removeDuplicates(flatten(outerop, innerop, nf1)))
    return answer


def nnfOf(btree):
    """rebuilds a BEXPR tree into its NNF, where negations are moved
       inwards and absorbed into the relational operators, 
       RELOP = ("<=", ">=", "==", "!=", "<", ">")

       Returns a new tree that is the NNF of  btree
    """
    dualLOP = {"and": "or", "or": "and", "forall": "exists", "exists":"forall"}
    dualRELOP = {"==": "!=", "!=": "==", "<=": ">", ">=": "<", "<": ">=", ">": "<="}
    op = btree[0]
    if op in Parse.RELOP + Parse.LCONST :
        ans = btree  #done
    elif op in ("and", "or") :
        ans = [op, nnfOf(btree[1]), nnfOf(btree[2])]
    elif op in ("forall", "exists") :
        ans = [op, btree[1], btree[2], btree[3], nnfOf(btree[4])]
    elif op == "not" :
        innerop = btree[1][0]
        if innerop in Parse.RELOP :
            ans = [dualRELOP[innerop], btree[1][1], btree[1][2]]
        elif innerop in Parse.LCONST :  # True or False
            ans = {"True":["False"], "False":["True"]}[innerop]
        elif innerop == "not" :
            ans = nnfOf(btree[1][1])
        elif innerop in ("forall", "exists") :
            ans = [ dualLOP[innerop], btree[1][1], btree[1][2], btree[1][3],  \
                     nnfOf(["not", btree[1][4]]) ]
        else :   # binary logical op --- push negations inwards:
            ans = nnfOf([dualLOP[innerop], ["not", btree[1][1]], ["not", btree[1][2]]] )
    else :
        error("invalid logical expression" + str(btree))
        ans = []
    return ans


def nfOf(outerop, innerop, prop) :  # textbook, p. 60, calls this  CNF
    """moves the innerops  within the  outerop  clauses.  """
    op = prop[0]
    if op in (innerop, outerop) :
        tree1 =  nfOf(outerop, innerop, prop[1])
        tree2 =  nfOf(outerop, innerop, prop[2])
        if op == outerop :
            answer = [op, tree1, tree2]
        else : # op == innerop
            answer = distribute(outerop, innerop, tree1, tree2)
    else : # prop is a primitive
        answer = prop
    return answer


def distribute(outerop, innerop, p1, p2):  # textbook, p.61, calls this  DISTR
    """distribute  converts a proposition of form,   p1 innerop p2,
       where  p1  and  p2  are btrees already in nf, 
       into an answer in nf  via:
       (P11 outerop P12) innerop P2 -||- (P11 innerop P2) outerop (P12 nnerop P2)
    """
    if p1[0] == outerop :
        answer = [outerop, distribute(outerop, innerop, p1[1],p2), \
                           distribute(outerop, innerop, p1[2],p2)]
    elif  p2[0] == outerop :
        answer = [outerop, distribute(outerop, innerop,p1,p2[1]), \
                           distribute(outerop, innerop,p1,p2[2])]
    else :
        # since  p1 and p2 are both in nf, then both are
        # proper innerop-clauses, which can be appended }"""
        answer = [innerop, p1, p2]
    return answer


def flatten(outerop, innerop, prop) :
    """makes a list of lists by removing all occurrences of the ops
       returns a list of lists of props

       pre: prop is a nested-list in nf
       post: answer is  prop  reformatted as
             [ [d11, d21, ...], [d21, d22, ...], ..., [dn1, dn2, ...]]
             where the innerop operators are implicit in the nested lists,
             and the outerop operators are implicit in the top-level list.
    """
    # this is a helper function for the use of  flattenCNF  only:
    def flattenInner(prop) :
        """makes a list of primitive props from  prop, an innerop list .

           pre: prop is a nested list where are embedded operators are innerop
           post: ans  is a list of all the arguments of the innerops
        """
        if prop[0] == innerop :
            ans = flattenInner(prop[1]) + flattenInner(prop[2])
        else :  # a primitive relation
            ans = [prop]
        return ans

    if prop[0] == outerop :
        answer = flatten(outerop, innerop, prop[1]) + flatten(outerop, innerop, prop[2])
    elif prop[0] == innerop :
        answer = [flattenInner(prop[1]) + flattenInner(prop[2])]
    else :  # primitive relation
        answer = [[prop]]
    return answer


def removeDuplicates(prop):
    """removeDuplicates  removes from each clause duplicate
       occurrences of any "P" or "-P",  that is,
                [ ... [p,...,p,...] ...]  ==>  [ ... [...,p,...] ...].

       pre: prop  is in flattened nf
       post:  answer is an equivalent proposition with duplicates removed
    """

    def removeDuplicate(d) :
        """removes all duplicates from list  d"""
        ans = []
        for prim in d :
            if not(prim in ans):
                ans = [prim] + ans
        return ans

    return  map(lambda disjunctive_clause: removeDuplicate(disjunctive_clause), prop)
    

def removeOpposites(prop):
    """removeOpposites  removes all clauses of form, [ ..., P, ..., -P,... ]

       pre:  prop  is a flattened nf
       post: answer is prop  with  ``opposites clauses'' removed
    """
    # ans = filter(lambda distcl: not(isOpposite(distcl)),  prop)
    #return ans
    ans = []
    for clause in prop :
        if not(hasOpposite(clause)) :
            ans = ans + [clause]
    return ans
        


def hasOpposite(d):
    """examines list d to see if it contains both "P" and "-P" for some P"""

    # dictionaries that define elementary games on relational operators:
    negationOf = {"==": "!=", "!=": "==", "<": ">=", "<=": ">", ">": "<=", ">=": "<"}
    rotate = {"==": "==", "!=": "!=", "<": ">", "<=": ">=", ">": "<", ">=": "<="}

    for prim in d :
        if prim[0] in Parse.RELOP : # prim is [RELOP, etree1, etree2]
            opop = negationOf[prim[0]]
            if ([opop, prim[1], prim[2]] in d) or ([rotate[opop], prim[2], prim[1]] in d) :
                return True
    return False  # if we reached here, no opposites discovered


def conjunctionOf(factlist) :
    """builds a single btree that represents the conjunction
       of all the facts in factlist
    """
    if len(factlist) == 0 :
        ans = ["True"]
    elif len(factlist) == 1 :
        ans = factlist[0]
    else :  
        ans = ["and", factlist[0], conjunctionOf(factlist[1:])]
    return ans
