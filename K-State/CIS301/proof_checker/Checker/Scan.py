"""Scan provides functions for reading a Python program and
   scanning its lines.  Its interface is

    init : filename -> void  
    quit : void -> void
    write : string -> void
    readLine : void -> (textline, leading whitespace, tokentuple)

  There is a helper function,  scan,  which is not normally called from
  outside the module

  Protocol for correct use:
     init(filename)
     THEN
     ( tuple = readLine()  |  write(newtext)  )*
     THEN
     quit()
"""


# globals for scanner:
inputfile = ()
outputfile = ()
EOF = "\a" # ascii bell (-:
EOL = "\n"


def init(inputfilename) :
    """opens the file holding the program and opens the output file,
       which will hold the analyzed program
       param: filename - a string, the filename
    """
    global inputfile, outputfile

    dot = inputfilename.find(".")
    if dot != -1 :
       outputname = inputfilename[:dot] + "A" + inputfilename[dot:]
    else :
       outputname = inputfilename + "A"

    inputfile = open(inputfilename, "r")
    outputfile = open(outputname, "w")

def quit() :
    """closes all files"""
    inputfile.close()
    outputfile.close()

def write(text) :
    """writes  text,  a string, to the output file"""
    #print "Scan has been asked to write:", text
    outputfile.write(text)

def readLine() :
    """obtains next unread line of source text from the input file,
       scans it, and returns a triple:
       the line of text, its leading whitespace indent, and its tuple of tokens.

       Any whitespace, comments, etc., are included in returned textline.
    """
    tokens = ()
    ansline = ""
    while tokens == () :
        line = inputfile.readline()
        ansline = ansline + line
        text = line.lstrip()
        indent = line[:len(line)-len(text)]
        if line == "" : # end of file ?
            tokens = (EOF,)
            break       # quit tokenizing

        if text == "" or text[0] == "#" :  # no useful tokens?
            pass
        elif len(text) > 3  and  text[:3] == '"""'  and  text[3] != "{" :  #doc string?
            text = text[3:]
            # collect multiline string (comment)
            while (text.find('"""') == -1) :  # while not found closing """
                text = inputfile.readline()
                ansline = ansline + text
                if text == "" :   # premature end of file ?
                    write("SCAN ERROR: premature end of file within doc string" + EOL)
                    tokens = (EOF,)
                    break
        else :  # found a code or proof line
            tokens = scan(text)

    print ansline,
    return (ansline, indent, tokens)
    

###########################################################################

def scan(text) :
    """scan splits apart the symbols in string  text  into a tuple."""
    separators = ('"""{', '}"""', '"""', \
                  "==", "!=", "<=", ">=", \
                  "=", "<", ">", "#", "{", "}", "(", ")", \
                  ",", ".", ":", '"', "'", "+", "-", "*", "/", "%", "[", "]")
    whitespace =(" ", "\t", "\n", "\r")
    tokens = ()
    rest = text
    word = ""
    while rest != "" :
        symbol = ""
        for item in whitespace + separators :  
            if rest.find(item) == 0 :
                symbol = item
                break
        if symbol != "" :   # found a separator?
            if word != "" :
                tokens = tokens + (word,)
                word = ""
            if symbol == "#" :  # comment starting ?
                break           # then, no more tokens to build; quit loop
            if not(symbol in whitespace) :
                tokens = tokens + (symbol,)
            rest = rest[len(symbol):]
        else :
            word = word + rest[0]
            rest = rest[1:]

    if word != "" :
        tokens = tokens + (word,)

    return tokens

##################################################################

def main(filename) :
    """ test driver"""
    init(filename)
    while True :
       raw_input("Press Enter")
       """(textline, indent, tokens) = readLine()
       print "textlines:"
       print textline
       print "indent=", indent, "tokens =", tokens"""
       print readLine()


