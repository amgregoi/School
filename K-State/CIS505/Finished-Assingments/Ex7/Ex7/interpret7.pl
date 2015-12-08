
/* Complete interpreter --- scanner, parser, evaluator --- for a
   command language with variables.   

Sample use:

?- run.
Type program as a string followed by a period:
|: "x = 2 ; y = 0 ; while x : x = ( x - 1 ) ; y = ( y + 2 ) ; print x end".

Scanned program: x = 2 ; y = 0 ; while x : x = ( x - 1 ) ; y = ( y + 2 ) ; print x end 

Parse tree: [assign([120],num(2)),assign([121],num(0)),while(iden([120]),[assign([120],sub(iden([120]),num(1))),assign([121],add(iden([121]),num(2))),print([120])])]

Execution:
1
0
Final contents of memory
x == 0
y == 4

*/


/* Driver code:  ********************************************************/
/* REPAIR THE TWO POSITIONS MARKED BELOW  */
 
run :- write('Type program as a string followed by a period:'),
       nl,
       read(InputText),
       scan(InputText, "", [], WordList),
       write('Scanned program: '), writeWords(WordList),
       parseCmdList(WordList, Tree),
       write('Parse tree: '), write(Tree), nl,
       write('Execution:'), nl,
       evalProgram(Tree, [], Store),   /* FIX ME */
       write('Final contents of memory'), nl,
       printMemory(Store), !.  /* FIX ME */


/****************************************************************************
  Scanner:  this part divides a string into a list of words. 
  THIS IS FINISHED.  DO NOT ALTER.

  scan(InputText, CurrentWordBeingAssembled,  WordsCollectedSoFar, FinalAnswer)
        where  InputText  is the string to be broken into words
               CurrentWordBeingAssembled  is the next word to be added to
                 to the  WordsCollectedSoFar
               WordsCollectedSoFar  are the words extracted so far from the
                 input text
               FinalAnswer  will hold the final value of  WordsCollectedSoFar 
                 It will be returned as the definition's answer

  IMPORTANT: all words must be separated by 1+ blanks!

  Example:  ?- scan("( 2 + ( x + 3 ) )", "", [], AnsList)
            AnsList = ["(", "2", "+", "(", "x", "+", "3", ")", ")"]
*/

/* cases when we have processed all the input text: */
scan([], [], Words, Words).
scan([], CurrentWord, Words, Ans) :- append(Words, [CurrentWord], Ans).

/* cases when there are more input characters to read:  */
scan([Char|Rest], CurrentWord, Words, Ans) :- notBlank(Char),
                       append(CurrentWord, [Char], NewWord),
                       scan(Rest, NewWord, Words, Ans).

scan([Char|Rest], CurrentWord, Words, Ans) :- isBlank(Char),
                       flushCurrentWord(CurrentWord, Words, NewWords),
                       scan(Rest, "", NewWords, Ans).

/* helper function that moves a completely assembled current word to the
     list of words collected so far:  */
flushCurrentWord("", Words, Words).
flushCurrentWord(Word, Words, NewWords) :- append(Words, [Word], NewWords).
/* a blank space is  Ascii code  32:  */
notBlank(C) :- C \= 32.
isBlank(32).

/* How to write a list of words to the output screen: */
writeWords([]) :- nl.
writeWords([H|T]) :- writeWord(H), writeWords(T).

writeWord([]) :- put(32).
writeWord([L|Rest]) :- put(L), writeWord(Rest).


/****************************************************************************
   Parser:  This part converts a list of words to a parse tree 
     (an operator tree).  
   WRITE THE MISSING CLAUSES FOR PARSING COMMANDS. 

Here is the input syntax it enforces:

   CL : CommandList      C: Command
   E : Expression        N : Numeral        I : Identifier

   CL ::= C ; CL | C
   C  ::= I = E  |  print I  | while E : CL end
   E ::=  N  |  I  |  ( E1 + E2 )
   N  is a string of digits
   I  is a string of lower-case letters

The parser outputs operator trees of these forms:

    PROGRAM == CLIST ::=  [ CTREE,* ]
       that is, a list of zero or more CTREEs
    CTREE ::=  assign(I, ETREE)  |  print(I)  |  while(ETREE, CLIST)
    ETREE ::=  num(N)  |  iden(I)  
            |  add( ETREE1, ETREE2 )   |  sub( ETREE1, ETREE2 )
    N ::= an integer
    I ::= a string


The clauses below match the grammar rules; they build a parse tree by guessing
possible "splittings" of the input wordlist into  subtrees that would be
combined into the final parse tree. 
*/


parseCmdList([], CL) :- write('Parse error: no input left').

parseCmdList(Words, [CTree|CL]) :-	
            /* split up  Words  into   CWords + [";"] + CLWords  :  */
            append(CWords, W1, Words),
            append([";"], CLWords, W1),
            parseCmd(CWords, CTree),
            parseCmdList(CLWords, CL).

parseCmdList(Words, [CTree]) :- 
            parseCmd(Words, CTree).
			


parseCmd([], CTree) :- write('Parse error: no input left').


            /* split Words into  ["while"] + E + [":"] + CL +  ["end"] : */
parseCmd(Words, while(ETree, CList)) :-
			append(W1,W3,Words), append(["while"], ETree1, W1), append([":"],CList1, W2), append(W2,["end"],W3), parseExpr(ETree1, ETree), parseCmd(CList1, CList).

            /* split up  Words  into   [I] + ["="] + E  :  */
parseCmd(Words, assign(I, ETree)) :- 
				append(I1, R1, Words), append(["="], E1, R1), parseExpr(I1, I), parseExpr(E1, Etree), nl.

           /* split up  Words  into  ["print"] + [I]  :  */
parseCmd(Words, print(I)) :- append(["print"], E1, Words), parseExpr(E1, I),nl.


parseExpr([], Tree) :- write('Parse error: no input left').
parseExpr([Word], num(Num)) :- isNum(Word), toInt(Word, F, Num). 
parseExpr([Word], iden(Word)) :- isIden(Word).  
parseExpr(Words, add(Tree1, Tree2)) :-  
             /* split up  Words  into  ["("] + E1 + ["+"] + E2 + [")"] :  */
             append(["("], W1, Words),
             append(E1, ["+"|W2], W1),
             append(E2, [")"], W2),
             /* You can write them out to see how  Words  got chopped up: */
             /* write('W1: '), write(W1), nl,
                write('W2: '), write(W2), nl,
                write('W3: '), write(W3), nl, nl,  */
             parseExpr(E1, Tree1),
             parseExpr(E2, Tree2).

parseExpr(Words, sub(Tree1, Tree2)) :-  
             /* split up  Words  into  ["("] + E1 + ["-"] + E2 + [")"] :  */
             append(["("], W1, Words),
             append(E1, ["-"|W2], W1),
             append(E2, [")"], W2),
             /* write('W1: '), write(W1), nl,
                write('W2: '), write(W2), nl,
                write('W3: '), write(W3), nl, nl,  */
             parseExpr(E1, Tree1),
             parseExpr(E2, Tree2).


/* Defines when a string is a numeral, that is, all digits: */
isNum([H]) :- isdigit(H).
isNum([H|T]) :- isdigit(H), isNum(T).
isdigit(N) :- N >= 48, N =< 57.

/* Defines when a string is an identifier, that is, all lower-case letters: */
isIden([H]) :- isLetter(H).
isIden([H|T]) :- isLetter(H), isIden(T).
isLetter(L) :- L >= 97,  L =< 122.  

/* Converts a string of digits,  NumeralString,  to an int,  AnswerInt:
   Call it like this:
      ?- toInt(NumeralString, F, AnswerInt)
         The  F  is a "local variable" that is not part of the answer. */
toInt([], 1, 0).
toInt([H|T], Factor, Val) :-  toInt(T, Fac, Val0),
                    HVal0 is H - 48,
                    HVal is HVal0 * Fac,
                    Val is HVal + Val0,
                    Factor is Fac * 10.


/****************************************************************************/
/* WRITE THIS PART, BASED ON HOW YOU MODEL THE INFORMATION IN MEMORY */


/* printMemory(PossibleMemoryArg)  displays the contents of "memory"
    IMPORTANT: use   writef(VARNAME)  to print the string, VARNAME,
       e.g.,  writef([120, 121])  prints   xy  on the display.

    IMPORTANT: If you model memory as a set of prolog predicates, use
       retractall  and  asserta  to implement assignment, like in Question 2
       of Exercise 6.   Use  findall  to help print the memory.

     If you model memory as a list data structure, use helper definitions
     like   lookup(I, []) :- ....
            lookup(I, [(Var,Value)|Rest], ...) :- ....
     like you did in Question 3 of Exercise 6 to do lookups, updates, and
     print memory.
	 printMemory(PossibleMemoryArg) :-  write('PRINT MEMORY CONTENTS HERE'), nl.
*/

/* couldn't get Val to print properly */

printMemory([]).
printMemory([[Key|Val]]) :- writef(Key), write(' = '), write(Val).
printMemory([[Key|Val]|T]) :- writef(Key), write(' = '), write(Val), nl, printMemory(T).



/***************************************************************************
  Interpreter:  This part computes the meaning of a parse tree.

  SUPPLY THE MISSING DEFINITIONS FOR COMMANDS AND EXPRESSIONS.

  Here are the forms of tree generated by the parser:

    PROGRAM == CLIST ::=  [ CTREE,* ]
       that is, a program is a list of zero or more CTREEs
    CTREE ::=  assign(I, ETREE)  |  print(I)  |  while(ETREE, CLIST)
    ETREE ::=  num(N)  |  iden(I)  
            |  add( ETREE1, ETREE2 )   |  sub( ETREE1, ETREE2 )
    N ::= an integer
    I ::= a double-quoted string

*/

/* evalProgram(CLIST, ...)  holds when program CLIST executes correctly. */
evalProgram(CLIST, In, Out)  :- evalCmdList(CLIST, In, Out).  /* FIX ME */

whileDecrement(Now, Next) :- Now \= 0, Next is Now - 1.
evalCmd(assign(iden(I), E1), OldStore, NewStore) :- evalExpr(E1, OldStore, Ans), update(I, Ans, OldStore, NewStore).
evalCmd(print(iden(I)), OldStore, NewStore) :- lookup(I, OldStore, Ans), write(Ans), nl.
evalCmd(while(I1, CL), OldStore, NewStore) :- write('while is wrong'), nl, evalCmdList(CL, OldStore, TempStore, _), evalExpr(lookup(I1, OldStore, A), OldStore, A), whileDecrement(A, Now), evalCmd(whileDecrement(num(Now), CL), TempStore, NewStore).




/* HERE ARE TWO FORMS OF  evalCmdList.   The one you use depends on how
   you choose to model the "memory"'s information.  
evalCmdList(CLIST, MoreStuff):-  write('REMOVE ME AND FINISH EVALUATOR'), nl, !.

 CHOOSE ONE OF THESE TWO VARIANTS:  

evalCmdList(CLIST)  holds true when  CLIST executes correctly,
   updating the memory "database"
evalCmdList([]).
evalCmdList([C|Rest]) :-  evalCmd(C), evalCmdList(Rest).

 evalCmdList(CLIST, In, Out)  holds true when  CLIST  executes with input
    memory vector,  In,  and computes output memory vector,  Out.   */
	
evalCmdList([], Mem, Mem).
evalCmdList([C|Rest], InMem, OutMem) :- evalCmd(C, InMem, MidMem), evalCmdList(Rest, MidMem, OutMem).
evalCmdList([C|Rest], InMem, OutMem) :- evalExpr(C, InMem), evalCmdList(Rest, InMem, OutMem).
evalCmdList([C|Rest], InMem, OutMem) :- evalCmdList(C, InMem, TOut), evalCmdList(Reset, TOut, OutMem).
evalCmdList(C, InMem, OutMem) :- evalCmd(C, InMem, OutMem).

									 
/* NOW, DEFINE  evalCmd  APPROPRIATELY.   NOTE THE THREE FORMS OF  
   CTREE  DEFINED ABOVE.
 
   You can obtain the code for  evalExpr  from  interpret.pl  
   or from  interpretStore.pl. REMEMBER to implement subtraction as well.
 */
evalExpr(num(N), Store, N).
evalExpr(iden(I), Store, Ans) :- lookup(I, Store, Ans).
evalExpr(add(E1, E2), Store, Ans) :- nl, evalExpr(E1, Store, Ans1), evalExpr(E2, Store, Ans2), Ans is Ans1 + Ans2
evalExpr(sub(E1, E2), Store, Ans) :- evalExpr(E1, Store, Ans1),  evalExpr(E2, Store, Ans2), Ans is Ans1 - Ans2.

lookup(I, [[I|V]|T], Ans) :- nl, write('I cannot get lookup to work'), nl, nl, Ans is V.
lookup(I, [[K|V]|T], Ans) :- lookup(I, T, Ans).

/* Update */
update(K,V,[[K|Val]|T], Store) :- Store = [[K|V]|T].
update(K,V,[[Key|Val]|T], Store) :- Store = [[Key|Val]|S], update(K,V,T,S).
update(K,V,[], Store) :- Store = [[K|V]].


