
"""run.py  runs the entire system, calling the parser and
   then the interpreter
"""

try:
    import parse
    import interpret
    tree = parse.parse()
    print "Parse tree:"
    print tree
    print "Execution:"
    interpret.main(tree)
except:  # an error:
  import traceback
  traceback.print_exc()
print
raw_input("press Enter key to finish")


