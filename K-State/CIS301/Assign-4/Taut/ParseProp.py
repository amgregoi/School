### Andy Gregoire / David Parker
### ParseProp.py
""" scanner and parser for propositional logic

    Grammar of propositions:

    PROP ::= PRIM  |  ~ PROP  |  ( PROP OP PROP )
    OP ::=  ^  |  v 
    PRIM ::=  T  |  F  |  VAR
    VAR is a single lower-case letter (but not "v" !)

    Operator trees (parse trees) generated from the above grammar:

    PTREE ::=  PRIM  |  ["~", PTREE}  |  ["^", PTREE1, PTREE2]  |  ["v", PTREE1, PTREE2]
    PRIM is "T" or "F" or a one-letter string (but not  "v") 
"""

def scan(text) :
    """scan splits apart the symbols in  text  into a list.

       pre:  text is a string holding a proposition
       post: answer is a list of the words and symbols within  text
             (spaces and newlines are removed)
             Example:   scan("(p ^ T ))")  returns   ["(", "p", "^", "T", ")", ")"]
       returns: answer
    """
    OPERATORS = ("(", ")", "^", "~", "v")  # must be one-symbol operators
    SPACES = (" ", "\n")
    SEPARATORS = OPERATORS + SPACES
 
    nextword = ""  # the next symbol/word to be added to the answer list
    answer = []

    for letter in text:
        # invariant:  answer + nextword + letter  equals all the words/symbols
        #     read so far from  text  with  SPACES  removed

        # see if  nextword  is complete and should be appended to answer:
        if letter in SEPARATORS  and  nextword != "" :
            answer.append(nextword)
            nextword = ""

        if letter in OPERATORS :
            answer.append(letter)
        elif letter in SPACES :
            pass  # discard space
        else :    # build a word or numeral
            nextword = nextword + letter

    if nextword != "" :   
        answer.append(nextword)

    return answer


########## Parser

# These global variables are initialized in the main driver procedure:

wordlist = []  # holds the remaining unread words
nextword = ""  # holds the first unread word
# global invariant:  nextword + wordlist == all remaining unread words

EOF = "!"      # a word that marks the end of the input words

def getNextword() :
    """moves the front word in  wordlist  to  nextword.
       If wordlist is empty, sets  nextword = EOF
       pre: True    post:  nextword == wordlist_in[0]  and  wordlist == wordlist_in[1:]
    """
    global nextword, wordlist
    if wordlist == [] :
        nextword = EOF
    else :
        nextword = wordlist[0]
        wordlist = wordlist[1:]


def parsePROP() :
    """builds a PTREE from the words in  nextword + wordlist,  where
          PROP ::= PRIM  |  ~ PROP  |  ( PROP OP PROP )
          OP ::=  ^  |  v 
          PRIM ::=  T  |  F  |  VAR
          VAR is a single lower-case letter
       also, maintains the global invariant (on wordlist and nextword)
       pre: True      
       post:  ans  is a parse tree of this format:
              PTREE ::=  PRIM  |  ["~", PTREE}  |  ["^", PTREE1, PTREE2]  |  ["v", Ptree1, PTREE2]
       returns: ans
    """
    def isPrim(word) :
        """helper function that examines  word  and returns True when  word
           is "T" or "F" or a single lower-case letter
           pre:  word is a string
           post: ans ==  (word is a legal  PRIM)
           returns: ans"""
        return  word == "T" or word == "F" or (len(word) == 1 and word.islower() and word != "v")  

    # code for  parseProp starts here:
    if isPrim(nextword) :    # PRIM ?
        ans = nextword
        getNextword()
    elif nextword == "~" :   # ~ PROP ?
        getNextword()
        tree = parsePROP()
        ans = ["~", tree]
    elif nextword == "(" :     # ( op EXPR ) ?
        getNextword()
        tree1 = parsePROP()
        op = nextword
        if op == "^" or op == "v": 
            getNextword()
            tree2 = parsePROP()
            if nextword == ")" :
                ans = [op, tree1, tree2]
                getNextword()
            else :
                error("missing )")
        else :
            error("illegal binary logical operator")
    else :
        error("illegal symbol to start a proposition")

    return ans


def error(message) :
    """prints an error message and halts the parse"""
    print "parse error: " + message
    print nextword, wordlist
    raise Exception




#### MAIN DRIVER:


def main(text) :
    """builds a parse tree (operator tree) for the proposition coded
       in the string,  text

       pre:  text  is a string
       post: returns the constructed tree
       returns: tree
    """
    global wordlist
    # read the input text, break into words, and place into wordlist:
    wordlist = scan(text)

    # do the parse:
    getNextword()  
    tree = parsePROP()
    if nextword != EOF :
       error("there are extra words")
    return tree

