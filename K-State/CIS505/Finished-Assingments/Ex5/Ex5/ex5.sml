(* DRIVER FOR INTERPRETER FOR MINI-C LANGUAGE WITH PROCEDURES *)

use "parser.sml";
use "interpreter.sml";

exception InputError;

(* collectText  reads the input program from the command window
   param:  inf - the function that reads one text line from the command window
   returns: a long string of all the lines typed
     collectText :  (Unit -> string) -> string
*)
fun collectText(inf) =
    let val txt = inf()
        in  if hd (explode txt) = #"!"
                 then ""
                 else txt ^ collectText(inf)
        end
;




(* The following two functions are written to read a line of user input from the
    terminal and return the input as a single string.
   Use the function that gets typed   unit -> string   by your ML implmentation.
*)
exception InputError;

fun in0() =
    TextIO.inputLine TextIO.stdIn
;

fun in1() =
    
    let val t = TextIO.inputLine TextIO.stdIn   (* read the line *)
    in  if isSome(t)                            (* if line is nonempty *)
        then valOf(t)
        else raise InputError
    end
;

(* run is the main driver.  Use it to run the parser-interpreter.
   param:  inf - the function that reads one text line from the command window
   returns: the final output Store from the input program's execution;
     Call it like this:   run(in1);
     or,                  run(in0);
     if the first option fails due to malformedness of  in1.
     See below for the functions,  in1  and  in0.
*)
fun run() =
    (print "\nType program below, terminated by ! as first symbol on the final line:\n";
    let val inputtext = collectText(in1)
        val tree = parse(inputtext)
    in
    (print "Parse tree:\n";
    print (Prog2string tree);
    print "\nExecution:\n";
    interpret(tree)
    )
    end)
;
