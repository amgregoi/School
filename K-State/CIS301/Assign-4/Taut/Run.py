
"""Run.py: Driver for evaluator/tautology checker"""

import sys, traceback  # libraries of system routines (for exception handling)
try :
    import ParseProp
    import EvalProp

    proposition = raw_input("Type a parenthesized proposition: ")
    tree = ParseProp.main(proposition)
    print "Parse tree is:"
    print tree
    print

    # COMMENT OUT THE FOLLOWING LINE WHEN ANSWERING QUESTIONS 2, 3, and 4 :
    #EvalProp.evalWithoutVars(tree)
    # UNCOMMENT THIS LINE FOR ANSWERING QUESTION 2 ONLY:
    #EvalProp.evalOneTest(tree)
    # UNCOMMENT THIS LINE FOR ANSWERING QUESTIONS 3 and 4 ONLY:
    EvalProp.evalAllTests(tree)

except:  # in the case of an error, do the following...
    print
    print "The program has crashed."
    print "Here is the execution trace, which lists the calls that led to the crash:"
    print
    traceback.print_exc(file=sys.stdout)

print
raw_input("Press Enter key to terminate the session")

