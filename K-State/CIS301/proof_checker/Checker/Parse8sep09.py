
"""Parser module.  Functions parse a line of python or embedded proof,
   producing an operator tree.
   Grammar rules and format of trees embedded in documentation of
   each parse function.

   Module interface:

   parseCOMMANDLINE : tuple of tokens -> (tree, unused tokens)
   parsePROOFLINE : tuple of tokens -> (tree, unused tokens)

"""

import Scan
EOF = Scan.EOF     # marks the end of the input
EOL = Scan.EOL
AOP = ("+", "-", "*", "/", "%")
RELOP = ("<=", ">=", "==", "!=", "<", ">")
LBINOP = ("and", "or")  # not yet "-->"
LUNOP = ("not",)
LCONST = ("True", "False")
PROOFWORDS = ("pre", "post", "return", "modifies", "invariant", "globalinv")
KEYWORDS = ("print", "while", "assert", "if", "else", "def", "return", "pass", "global", "len", "append", "raw_input") + PROOFWORDS + LBINOP + LUNOP + LCONST


######################################################################
"""global data structures and maintenance function: """
tokentuple = ()    # holds remaining unread tokens for input line
token = ""         # holds the next unread token

def getNext() :
    """moves the front token in  tokentuple  to  token.
       If empty, sets  token = EOF
    """
    global tokentuple, token
    if tokentuple == () :
        token = EOL
    else :
        token = tokentuple[0]
        tokentuple = tokentuple[1:]
    #print "token =", token


########################################################################
"""parser functions start here.  All share above global data structures.
   All follow usual recursive-descent format.

   Each returns a parse tree (operator tree) as its answer.
"""

def parseBEXPR() :
    """ BEXPR ::=  forall EXPR < VAR <= EXPR , BBEXPR  |  BBEXPR

        foralltree ::= ["forall", etree, ["var", v], etree, btree] |  btree
    """
    ans = []
    if token == "forall" :
        getNext()
        etreelo = parseEXPR()
        if token == "<=" :
            getNext()
            if isVar(token) :
                indexname = token
                getNext()
                if token == "<" :
                   getNext()
                   etreehi = parseEXPR()
                   if token == "," :
                       getNext()
                       btree = parseBBEXPR()
                       ans = ["forall", etreelo, ["var", indexname], etreehi, btree]
        if ans == [] :
            error("incorrect syntax for  forall;  should be:\n  forall EXPR < VAR < EXPR, BEXPR")
    elif token == "for" :
        error("sorry --- you must spell it as 'forall', not 'for all'")
    else :
        ans = parseBBEXPR()
    return ans


def parseBBEXPR() :
    """ BEBXPR ::=  NEXPR LBINOP NEXPR |  NEXPR
        LBINOP ::= "and" | "or"    (no implies for now)

        btree ::= [LBINOP, ntree1, ntree2] |  ntree
    """
    tree1 = parseNEXPR()
    if token in LBINOP :
        op = token
        getNext()
        ans = [op, tree1, parseNEXPR()]
    else :
        ans = tree1
    return ans

def parseNEXPR() :
    """ NEXPR ::= LUNOP REXPR | REXPR
        LUNOP ::= not
    
        ntree ::= [LUNOP, rtree]  |  rtree
    """
    if token in LUNOP :
        op = token
        getNext()
        tree = parseREXPR()
        ans = [op, tree]
    else :
        ans = parseREXPR()
    return ans

def parseREXPR() :
    """ REXPR ::= EXPR RELOP EXPR | EXPR | True | False
        RELOP ::=  == | != | < | <= | > | >= 

        rtree :== [RELOP, etree1, etree2]  |  etree | ["True"] | ["False"]
    """
    if token in ("True", "False") :
        ans = [token]
        getNext()
    else :
        tree1 = parseEXPR()
        if token in RELOP :
            op = token
            getNext()
            ans = [op, tree1, parseEXPR()]
        else :
            ans = tree1
    return ans

def parseEXPR() :
    """ EXPR ::= TERM AOP TERM | TERM
                 AOP is "+" or "-" or "*"
        etree :== [AOP, ttree1, ttree2]  |  ttree
    """
    tree1 = parseTERM()
    if token in AOP :
        op = token
        getNext()
        ans = [op, tree1, parseTERM()]
    else :
        ans = tree1
    return ans

def parseTERM() :
    """ TERM ::= VAR  |  VAR ( EXPRLIST ) | NUM | ( BEXPR )
               | VAR [ EXPR ]  |  len( VAR )  |  [ EXPRLIST ]  

        must improve later to accommodate and list indexing
                 VAR [ EXPR ]
       
        ttree ::=  ["var", VAR] | ["call", VAR, etreelist] 
                 | ["int", NUM] | btree | ["index", ["var", VAR], etree]
                 | ["len", ["var", VAR]] |  ["list", etreelist ]
    """
    ans = []
    if isVar(token) :
        v = token
        getNext()
        if token == "(" :
            getNext()
            elist = parseEXPRLIST()
            ans = ["call", v, elist]
            if token == ")" :
               getNext()
            else :
               error("missing right paren for function call")
        elif token == "[" :
            getNext()
            ans = ["index", ["var", v], parseEXPR()]
            if token == "]" :
                getNext()
            else : error("expecting ]")
        else : 
            ans = ["var", v]
    elif token == "len" :
        getNext()
        if token == "(" :
            getNext()
            if isVar(token) :
                ans = ["len", ["var", token]]
                getNext()
                if token == ")" :
                    getNext()
                else : error("expecting )")
            else : error("expecting var name")
        else : error("can't use  len  as a var name")
    #elif token == "readInt" :
    #    ans = ["readInt"]
    #    getNext()
    #    if token == "(" :
    #        getNext()
    #        if token == ")" :
    #            getNext()
    #        else : error("expecting )")
    #    else : error("expecting (")
    elif isNum(token) :
        ans = ["int", token]
        getNext()
    elif token == "(" :
        getNext()
        tree = parseBEXPR()
        ans = tree
        if token == ")" :
            getNext()
        else :
            error("missing ')'")
    elif token == "[" :
        getNext()
        ans = ["list", parseEXPRLIST()]
        if token == "]" :
            getNext()
        else :
            error("missing ]")
    else :
        error("invalid expression")
    return ans


def parseEXPRLIST() :
    """ EXPRLIST ::= \epsilon | EXPR , EXPRLIST
        elist ::= list of 0+ etrees
    """
    ans = []
    while token not in ( ")", "]") :
        ans.append(parseEXPR())
        if token == "," :
            getNext()
    return ans


##############################################################

def parseCMD():
    """ CMD ::= LHS = EXPR |  if BEXPR :  |  else : |  while BEXPR :
              | assert BEXPR | pass  |  def VAR ( VARLIST ) :  | return [VAR]
              | global VARLIST  | print TRASH
              | LHS . append ( EXPR )

        ctree ::=  ["=", vtree, etree]  | ["if", btree]  | ["else"]
                |  ["while", btree]  |  ["assert", btree]  |  ["pass"]
                |  ["def", vtree, vtreelist ]  |  ["return"]
                |  ["return", vtree]  |  ["global", vtreelist ]
                |  ["print"]  | ["raw_input"]
                |  ["append", ["var", VAR], etree]
    """
    ans = []
    if token == "if" :
        getNext()
        tree = parseBEXPR()
        ans = ["if", tree]
        if token == ":" : getNext()
        else : error("missing : for 'if'")
    elif token == "else" :
        ans = ["else"]
        getNext()
        if token == ":" : getNext()
        else : error("missing : for 'else'")
        getNext()
    elif token == "while" :
        getNext()
        tree = parseBEXPR()
        ans = ["while", tree]
        if token == ":" : getNext()
        else : error("missing : for 'while'")
    elif token == "assert" :
        getNext()
        tree = parseBEXPR()
        ans = ["assert", tree]
    elif token == "pass" :
        ans = ["pass"]
        getNext()
    elif token in ("print", "raw_input") :
        ans = [token]
        getNext()
    elif token == "def" :
        ans = []
        getNext()
        if isVar(token) :
            fname = token
            getNext()
            if token == "(" :
                getNext()
                ans = ["def", fname, parseVARLIST()]
                if token == ")" :
                    getNext()
                    if token == ":" :
                        getNext()
                    else :
                        error("missing colon for function defn")
                else :
                    error("missing right paren on function defn")
            else :
                error("missing left paren on function defn")
        else :
            error("missing function name on function defn")
    elif token == "return" :
        getNext()
        if isVar(token) :
            ans = ["return", ["var", token]]
            getNext()
        else :
            ans = ["return"]
    elif token == "global" :
        getNext()
        ans = ["global", parseVARLIST()]
    elif isVar(token) :  # assignment
        tree1 = parseLHS()
        if token == "=" :
            getNext()
            ans = ["=", tree1, parseEXPR()]
        elif token == "." :
            ans = tree1 # for the moment
            getNext()
            if token == "append" :
                getNext()
                if token == "(" :
                    getNext()
                    ans = ["append", tree1, parseEXPR()]
                    if token == ")" :
                        getNext()
                    else :
                        error("expecting )")
                else :
                    error("expecting (")
            else :
                error("only  append  is supported.  Sorry")
        else :
            error("invalid command")
    else : error("invalid command")
    return ans


def parseLHS() :
    """ LHS ::= VAR |  VAR [ EXPR ]
        lhstree ::= ["var", VAR]  |  ["index" , ["var", VAR],  etree]
    """
    if isVar(token) :
        namepart = ["var", token]
        getNext()
        if token == "[" :
            getNext()
            ans = ["index", namepart, parseEXPR()]
            if token == "]" :
               getNext()
            else :
               error("missing ]")
        else :
            ans = namepart
    else :
        error("expecting Variable reference")
        ans = []
    return ans


def parsePF():
    """ PF ::=  invariant BEXPR  |  modifies VARLIST |  NUM .  BEXPR  JUST
             |  pre BEXPR  |  post BEXPR  |  return VAR | globalinv BEXPR
             |  def BEXPR

        pftree ::=  ["invariant",  btree]  |  ["modifies", vlist]
                 |  [NUM, btree, jtree]  |  ["pre" btree]  |  ["post" btree]
                 |  ["return", VAR]  |  ["globalinv", btree
    """
    ans = []
    if token in ( "invariant", "pre", "post", "globalinv", "def") :
        op = token
        getNext()
        ans = [op, parseBEXPR()]
    elif token == "modifies" :
        getNext()
        ans = ["modifies", parseVARLIST()]
    elif token == "return" :
        getNext()
        if isVar(token) :
            ans = ["return", ["var", token]]
            getNext()
        else :
            error("function must return a variable. Sorry.")
            ans = []
    elif isNum(token) :
        num = token
        getNext()
        if token != "." :
            error("expecting . after line number")
        else :
            getNext()
            if token == "return" :  # return (andi) multiple facts
                getNext()
                ans = ["return"]
                while isNum(token) :
                    ans.append(token)
                    getNext()
            else : # normal proof line:
                tree1 = parseBEXPR()
                ans = [num, tree1, parseJUST()]
    else :
        error("proof line begins incorrectly")
    return ans

def parseVARLIST() :
    """ VARLIST ::= \epsilon | VAR , VARLIST
        vlist ::= list of 0+ VARs
    """
    ans = []
    while isVar(token) :
        ans.append(["var", token])
        getNext()
        if token == "," :
            getNext()
    return ans
            
def parseJUST() :
    """ JUST ::=  premise | algebra NUM* 
               | andi NUM NUM | ande NUM | ori NUM | ore NUM
               | copy NUM   |  globalinv  | subst NUM*  | substindex NUM
               | foralli NUM*  | foralle EXPR NUM*
               | def
        
        jtree ::= ["premise"] | ["copy", NUM] |
               |  ["algebra", NUM*]
               |  ["op", NUM] where op in {ori, ande, ore}
               |  ["op", NUM, NUM] where op in {andi}
               |  ["globalinv"] | ["foralli", NUM*]  |  ["foralle", etree, NUM*]
               |  ["substforall", NUM]  | ["def"]
    """
    if token in ("premise", "globalinv", "def") :
        ans = [token]
        getNext()
    elif token in ("copy", "substindex") :
        op = token
        getNext()
        if isNum(token) :
            ans = [op, token]
            getNext()
        else :
            ans = [op, ""]
            error(op + " requires a line number")
    elif token == "subst" :
        ans = ["subst"]
        getNext()
        while isNum(token) :
            ans.append(token)
            getNext()
        if len(ans) != 3 :
            error("subst requires exactly two line numbers")
            ans.append("")
            ans.append("")
    elif token in ("algebra", "foralli") :
        ans = [token]
        getNext()
        while isNum(token) :
            ans.append(token)
            getNext()
    elif token == "foralle" :
        ans = [token]
        getNext()
        ans.append(parseEXPR())   # index expression for  foralle
        while isNum(token) :
            ans.append(token)
            getNext()
    elif token == "andi" :
        ans = ["andi"]
        getNext()
        while isNum(token) :
            ans.append(token)
            getNext()
        if len(ans) < 3 :
            error("andi requires two line numbers")
            ans.append("")
            ans.append("")
    elif (token == "ande") or (token == "ori") or (token == "ore") :
        op = token
        getNext()
        if isNum(token) :
            ans = [op, token]
            getNext()
        else :
            error(op + " requires a line number")
            ans = [op, ""]
    else : 
        error("invalid justification or malformed assertion")
        ans = []

    return ans


def error(message) :
    m = "PARSE ERROR " + message + " at token:"
    print m, token, tokentuple
    Scan.write(m + EOL)
    raise ParseException
    #Analyze.setError(m)


def isVar(word) :
    """checks if word is a legal id;  param word is a string of 1+ chars"""
    #return ( word.isalpha()  and  not(word in KEYWORDS) )
    ans = not(word in KEYWORDS) and (word[0] == "_" or word[0].isalpha())
    for ch in word :
        ans = ans and (ch.isalpha() or ch == "_" or ch.isdigit())
    return ans
       

def isNum(word) :
    return word.isdigit()


#####################################################################
"""here is a little library of functions that rebuild existing optrees"""


### convert-to-string functions: flattens an optree into a string

def tostringBexpr(btree):
    """converts contents of boolean expr tree into a string"""
    ans = ""
    if btree[0] in LCONST :  # True or False
        ans = btree[0]
    elif btree[0] in LBINOP :   # and, or
        ans = "(" + tostringBexpr(btree[1]) + " " + btree[0] + " " + tostringBexpr(btree[2]) + ")"
    elif btree[0] in LUNOP :  # not
        ans = btree[0] + " " + tostringBexpr(btree[1])
    elif btree[0] in RELOP :  # relational expression, e.g., a < b
        ans =  "(" + tostringExpr(btree[1]) + " " + btree[0] + " " + tostringExpr(btree[2]) + ")"
    elif btree[0] == "forall" :
        lo = tostringExpr(btree[1])
        i = btree[2][1]
        hi = tostringExpr(btree[3])
        body = tostringBexpr(btree[4])
        #ans = "forall(" + lo +", "+ hi +", "+ "lambda " + i + ": " + body + ")"
        ans = "forall " + lo + " <= " + i + " < " + hi + ", " + body
    elif btree[0] == "isinstance" :
        ans = "isinstance(" + tostringExpr(btree[1]) + ", " + btree[2] + ")"
    elif btree[0] == "call" :
        ans = btree[1] +"("+ tostringExprlist(btree[2]) +")"
    else :
        ans = "toStringErrBexpr" + str(btree)
    return ans


def tostringExpr(etree):
    """converts contents of expr tree into a string"""
    ans = ""
    if etree[0] in AOP :   # +,-,*, etc
        ans = "(" + tostringExpr(etree[1]) + " " + etree[0] + " " + tostringExpr(etree[2]) + ")"
    elif etree[0] == "var" :  
        ans = etree[1]
    elif etree[0] == "int" :
        ans = etree[1]
    elif etree[0] == "index" :
        ans = etree[1][1] + "[" + tostringExpr(etree[2]) + "]"
    elif etree[0] == "list" :
        ans = "[" + tostringExprlist(etree[1]) + "]"
    elif etree[0] == "len" :
        ans = "len(" + tostringExpr(etree[1]) + ")"
    elif etree[0] == "call" :
        ans = etree[1] +"("+ tostringExprlist(etree[2]) +")"

    elif etree[0] == "readInt" :
        ans = "readInt()"
    else :
        ans = "toStringErrExpr " + str(etree)
    return ans

def tostringExprlist(elist):
    """converts a list of  etrees to a string """
    ans = ""
    for i in range(len(elist)) :
        ans = ans + tostringExpr(elist[i])
        if i != len(elist)-1 :  ans = ans + ", "
    return ans


def tostringVarlist(varlist):
    """converts a list of ["var", v]s  and ["index", vtree, etree]s
       to a string """
    ans = ""
    for i in range(len(varlist)):
        item = varlist[i]
        if item[0] == "var" :
            ans = ans + " " + item[1]
        elif item[0] == "index" :
            ans = ans + " " + item[1][1] + "[" + tostringExpr(item[2]) + "]"
        if i != len(varlist) - 1 :
            ans = ans + ","
    return ans


####functions that do substitution and rebuild trees:

def makeVar(v) :
    """from string, v,  constructs and returns  ["var", v]"""
    return ["var", v]

def makeOldVar(v) :
    """from var, v == ["var", name], constructs and returns ["var", name_old]"""
    if v[0] == "var" :
        ans = ["var", v[1] + "_old"]
    else : ans = []
    return ans

def makeInVar(v) :
    """from var, v == ["var", name], constructs and returns ["var", name_in]"""
    if v[0] == "var" :
        ans = ["var", v[1] + "_in"]
    else : ans = []
    return ans

def conjunctionOf(btreetuple) :
    """rebuilds a tuple of btrees (BEXPR trees) into one wellformed btree that
       denotes the conjunction of the trees
    """
    if len(btreetuple) == 0 :
        ans = ["True"]
    else :
        i = len(btreetuple)-1
        ans = btreetuple[i]
        while i > 0 :
            i = i -1
            ans = ["and", btreetuple[i], ans]
    return ans




def substituteTree(replacement, pattern, tree):
    """substitutes all occurrences of  pattern  by  replacment in tree"""
    if tree == pattern :
        ans = replacement
    elif isinstance(tree, list) :
        ans = []
        for subtree in tree :
            ans.append(substituteTree(replacement, pattern, subtree))
    else :
        ans = tree
    return ans

def substituteParallelTree(replaces, patterns, tree) :
    """forall 0 < i <= len(replaces),  replaces all occurrences of
         patterns[i] by replaces[i] in  tree  and returns the new tree
    """
    if len(replaces) < len(patterns) :
        error("substituteParallelTree: mismatch of patterns with replacements")
        return []
    # traverse tree and try to match subtrees against any of  patterns:
    if tree in patterns :
        for i in range(len(patterns)) :  # find which one...
            if tree == patterns[i] :
                ans = replaces[i]
                break
    elif isinstance(tree, list) :
        ans = []
        for subtree in tree :
            ans.append(substituteParallelTree(replaces, patterns, subtree))
    else :
        ans = tree
    return ans


def substituteIndex(replace, patt, tree) :
    """searches for all occurrence of  ["index", patt, _]  in tree
       and replaces them by  ["index", replace, _]

       returns a tree with the alterations
    """
    if not(isinstance(tree, list)) :
        ans = tree
    elif len(tree) > 0 and tree[0] == "index" and  tree[1] == patt :
        ans = ["index", replace, tree[2]]
    else :
        ans = []
        for subtree in tree :
            ans.append(substituteIndex(replace, patt, subtree))
    return ans


def foundIn(pattern, tree):
    """searches for an occurrence of pattern  _anywhere_ in  tree"""
    ans = False
    if tree == pattern :
        ans = True
    elif isinstance(tree, list) :
        for subtree in tree :
           ans = ans or foundIn(pattern, subtree)
    else :
        ans = False
    return ans


def foundArrayRef(vtree, btree):
    """searches to see if vtree  ["var",s]  appears in a context,
       ["index", vtree, _]  or  ["len", vtree]  within vtree
       Returns the outcome of the search
    """
    if not isinstance(vtree, list):
        return False
    elif (btree[0] == "index" or btree[0] == "len") and btree[1] == vtree :
        return True
    else :
        for clause in btree[1:] :
            if foundArrayRef(vtree, clause) :
                return True
        # if we reach here, vtree was not found
        return False


def match(matches, tree, scheme):
    """attempts to match  tree  to  scheme,  saving matches in  matches

       params: matches - a dictionary holding all matches of pattern vars,
                  ["var" v], to etrees made so far
               tree - the btree to be matched
               scheme - the btree whose vtrees are treated as pattern vars

       action: adds matches made to  matches;  returns True if tree is
       successfully matches to  scheme  consistent with info in matches.
    """
    if isinstance(tree, str):
        if isinstance(scheme, str) and  tree == scheme :
            return True
        else : return False

    #else, both are lists:
    top = tree[0]
    sop = scheme[0]

    if sop == "var" :  # a pattern var ?
        patvar = scheme[1]
        if patvar in matches :
            if matches[patvar] == tree :
                return True
            else : return False  # trying to match patvar two different ways
        else :  # first time  patvar  is being matched:
            matches[patvar] = tree
            return True

    # sop is not a pattern var, so we compare the two trees:
    if len(scheme) != len(tree) : return False   # a loser

    #else :
    ans = True
    for i in range(0, len(tree)) :
        ans = ans and match(matches, tree[i], scheme[i])
    return ans



def extractVarsFrom(vtree):
    """returns a list of all  ["var", s]  trees embedded within vtree"""
    if not isinstance(vtree, list):
        ans = []
    elif vtree[0] == "var" :
        ans = [ vtree ]
    else :
        ans = []
        for clause in vtree[1:] :
            ans = ans + extractVarsFrom(clause)
    return ans



def subtractVars(vlist1, vlist2):
    """returns a list of all vtrees in vlist1 that are not also in vlist2"""
    return [ vtree for vtree in vlist1 if  vtree not in vlist2 ]

def removeDuplicates(vlist):
    """returns a list that has all vtrees in vlist but no duplicates"""
    ans = []
    for vtree in vlist :
        if not vtree in ans :
           ans.append(vtree)
    return ans


####################################################################
#####################################################################
"""Driver functions:  These form the module's public interface.

   When called, each is supplied a tuple (one textline's worth) of tokens
   to parse.  

   Each returns the assembled operator tree plus any remaining tokens.
"""

def parseCOMMANDLINE(tokens):
    global tokentuple
    tokentuple = tokens
    getNext()
    tree = parseCMD()  
    return (tree, (token,) + tokentuple)

def parsePROOFLINE(tokens) :
    global tokentuple
    tokentuple = tokens
    getNext()
    tree = parsePF()
    return (tree, (token,) + tokentuple)


######################################################################
""" test driver:"""

def main(filename) :
    global tokentuple
    Scan.init(filename)
    while True :
       raw_input("Press Enter")
       print
       (textline, indent, tokens) = Scan.readLine()
       tree, rest = parseCOMMANDLINE(tokens) 
       Scan.write(textline)
       print "tree =", tree
       print "what's left over:", rest

def testmatch(filename) :
    global tokentuple
    Scan.init(filename)
    raw_input("Press Enter")
    print
    (textline, indent, tokens) = Scan.readLine()
    scheme, rest = parseCOMMANDLINE(tokens)
    Scan.write(textline)
    print "SCHEME =", scheme[1]
    print "what's left over:", rest

    raw_input("Press Enter")
    print
    (textline, indent, tokens) = Scan.readLine()
    tree, rest = parseCOMMANDLINE(tokens)
    Scan.write(textline)
    print "tree =", tree[1]
    print "what's left over:", rest

    matches = {}
    success = match(matches, tree[1],scheme[1])
    print "success = ", success
    print "matches =",  matches

