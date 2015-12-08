
Hello,

The CIS301 proof checker analyzes baby Python programs for correctness.
The checker is itself written in Python, and you must have Python
installed on your computer to use the checker. (All Mac and Linux machines
have Python, as do many Windows machines.  If your machine lacks
Python, you can download it for free.  See the information
on the CIS301 home page.)


The file, cis301.zip,  must be unzipped to expose the folder,  cis301.
Then, move/copy that folder from the compressed-file-window to its new
home on your computer.  (A good place is your  My Documents  folder
on a Windows machine.)

The cis301 folder contains this README file, a folder named  Checker,
that holds the checker, and two folders of program examples
that you can use as input to the checker: Exw (Windows format)
and Ex (Unix/linux format).   The folders differ
only in that the former has its text formatted in MS-DOS, which is readable
by all Windows editors, and the latter has its text formatted for
Unix editors (e.g., emacs, vi).

IMPORTANT: When you use the checker, it will be best to save the programs
you analyze in the  cis301  folder or placed in a folder that is
itself placed within the cis301 folder (e.g., just like the Exw and Ex folders).


The proof checker is designed so that you can start it from the
command line or you can double-click on its icon.  

IMPORTANT: it is best to make a shortcut icon to the checker
and start the checker by double-clicking on the shortcut.

1. In Windows XP, To generate a shortcut, open the  Checker folder,
right-click on  Check.py,  and select  ``Create Shortcut''.   Then,
move the shortcut icon to where you will find it most convenient to use.
(A good place is within the  cis301  folder or on your Desktop.)


2. To use the checker, double click on its shortcut.
This will generate an interactive session, where you are asked
the name of the file that you wish analyzed and any execution options.
Here is what you see if you start the checker and you check the file, 
Exw/while.py:  (For one moment, pretend your name is Smith and you
saved the  cis301  folder  in  C:\Documents and Settings\My Documents\Smith.)

+----
| Command-line usage: python Check.py [-args] FILENAME.py
   where  args  can be any or all of
      v : verbose mode: insert deduced asserts as comments in output
      a : include all possible asserts in proof output as premises
      x : insert header and assert code in output file for execution
      n : do not generate html file for viewing
      d : display internal data structures for debugging

   Entering interactive mode. (Press Enter to quit.)
   Current path is   C:\Documents and Settings\My Documents\Smith\cis301
   Type filename (relative to current path) to check:  Exw/while.py
   Type options (any or none of  vaxnd): v

     ... analysis is displayed here ...

|  Press  Enter to repeat with this file; Press  q  to quit:
+----

The checker locates the file at   
C:\Documents and Settings\My Documents\Smith\cis301\Exw\while.py,
analyzes it, and deposits the annotated results at
Exw/whileA.py.   There is also an html-version at  Exw/whileA.py.htm.
that is color-highlighted when viewed with a web browser.

At the same time that you are using the checker, use a text editor
to type/edit/revise the program you are analyzing and use a web browser
to study the results after each analysis.  (This is your ``development
environment.'')


3. You can now edit the program and try again by pressing  Enter  in the
program window.  In this way, you can edit and revise until you are
finished.


4. If you like working within a command window (this is true for
Linux and some Mac users), you can use the checker this way, too:
Make a new command window,  cd to  cis301, and type this at the
command line:
   python Checker/Check.py 

This starts the session.  If you prefer to use command-line arguments,
you may do so, like this:
    python Checker/Check.py -va Ex/while.py

This runs the checker only once, but you can restart it by
pressing the up-arrow key and Enter.


The modules inside the Checker folder are Python source code that you
can read and hack.  In particular, you can customize the input interface
by editing the main code in  Check.py.

