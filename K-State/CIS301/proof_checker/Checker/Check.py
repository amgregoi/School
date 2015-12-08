
"""Start up (Check) module for proof checker.
"""

########################################################################
# Here are a few naive functions that generate html output:

EOL = '\n'
RETURN = '\r'
proof_mode = False

def attachHeaderTo(outputstream):
    outputstream.write('<html><body><pre><strong>' + EOL)

def attachFooterTo(outputstream):
    outputstream.write('</strong></pre></body></html>' + EOL)

def format(line) :
    """a naive pattern matcher and substitution function"""
    global proof_mode
    comment_mode = False

    patterns = { "assert" : "#CD6600", \
                 "OK" : "#00FF00", \
                 "??" : "#EE2C2C", \
                 "UNABLE" : "#EE2C2C", \
                 "ERROR" : "#EE2C2C" }
    input = line
    output = ""
    while input != "" :
        if input[0] == "#" :
            if not comment_mode:
                output = output + '<font color="#1E90FF">'  # blue
                comment_mode = True
            output = output + input[0]
            input = input[1:]

        elif input.find('"""{') == 0 :
            output = output + '<font color="#008B00">"""{'
            proof_mode = True
            input = input[4:]
        elif input.find('}"""') == 0 :
            output = output + '}"""</font>'
            proof_mode = False
            input = input[4:]
        else :
            match = False
            for patt in patterns :
                if input.find(patt) == 0 :
                    output = output + '<font color="' + patterns[patt] \
                           + '">' + patt + '</font>'
                    input = input[len(patt):]
                    match = True
                    break  # do just one at a time, please
            if not match :
                output = output + input[0]
                input = input[1:]

    if comment_mode :
        index = output.find(RETURN)
        if index == -1 :
            index = output.find(EOL)
        if index == -1:
            output = output + '</font>'
        else :
            output = output[:index] + '</font>' + output[index:]

    return output


def generateHtml(filename) :
    """copies output file,  filename,  into an html-formatted file"""
    dot = filename.find(".")
    if dot != -1 :
       analyzedfilename = filename[:dot] + "A" + filename[dot:]
    else :
       analyzedfilename = inputfilename + "A"

    input = open(analyzedfilename, "r")
    output = open(analyzedfilename + ".htm" , "w") 

    attachHeaderTo(output)

    line = input.readline()
    while line != "" :
        newline = format(line)
        output.write(newline)
        line = input.readline()

    attachFooterTo(output)
    input.close()
    output.close()


######################################################################
### START-UP CODE #####################################################

import sys
import Analyze


html = True  # whether to generate an html file at the end
interactive = False   # whether startup was interactive or command-line
result = False  # did we get a useful result or an exception?

if len(sys.argv) < 2 :    # startup by double-click or command-line name only:
    print "Command-line usage: python Check.py [-args] FILENAME.py"
    print "where  args  can be any or all of"
    print "   v : verbose mode: insert deduced asserts as comments in output"
    print "   a : include all possible asserts in proof output as premises"
    print "   x : insert header and assert code in output file for execution"
    print "   n : do not generate html file for viewing"
    print "   d : display internal data structures for debugging"
    print
    print "Entering interactive mode. (Press Enter to quit.)"
    interactive = True

    import os
    cwd = os.getcwd()  # get current working dir
    if os.path.basename(cwd) == "Checker" : # is cwd the folder where this pgm lives?
        # then, move up one level; don't want to deposit junk here!
        os.chdir(os.pardir)
    print "Current path is ", os.getcwd()

    filename = raw_input("Type filename (relative to current path) to check: ")
    options = raw_input("Type options (any or none of  vaxnd): ")
    while filename != "" :
        result = Analyze.main(filename, options)
        if result and html :
            generateHtml(filename)
        print
        repeat = raw_input("Press  Enter  to repeat with this file; Press  q  to quit: ")
        if repeat == "q" : filename = ""

else :  # it's a command line startup with all info supplied
    if sys.argv[1][0] == "-" :
        filename = sys.argv[2]
        if "n" in sys.argv[1] :  html = False
        result = Analyze.main(filename, sys.argv[1])
    else :
        filename = sys.argv[1]
        result = Analyze.main(filename)

    if result and html :
        generateHtml(filename)

# Finished.

