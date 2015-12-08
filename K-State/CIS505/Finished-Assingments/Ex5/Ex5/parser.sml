(*  Scanner and parser for CIS505 Exercise 5.

PROGRAM ::=  DECLIST COMMANDLIST 
DECLIST ::=  DECLARATION ; DECLIST  |  (nothing)
DECLARATION ::=  int ID  |  proc ID ( IDLIST ) : COMMANDLIST end
COMMANDLIST ::=  COMMAND ; COMMANDLIST  |  (nothing)
COMMAND ::=  ID = EXPRESSSION
             |  print EXPRESSION
             |  while EXPRESSION : COMMANDLIST end
             |  call ID  ( ELIST ) 
ELIST ::=  EXPRESSION,*      that is,  zero or more  EXPRESSIONS separated by ,
EXPRESSION ::= NUMERAL  |  ID  |  ( EXPRESSION OPERATOR EXPRESSION )
OPERATOR is  +  or  -
NUMERAL  is a sequence of digits from the set, {0,1,2,...,9}
ILIST ::=  ID,*
ID  is a string of lower-case letters, not a keyword

The forms of output parse trees are as follows:
*)
type Id = string

datatype Exp =
  Num of int
| L of Id
| Add of Exp * Exp
| Sub of Exp * Exp

and Comm =
  Assign of Id * Exp
| Print of Exp
| While of Exp * (Comm list)
| Call0 of Id                 (* not used in this assignment; ignore it *)
| Call of Id * (Exp list)

and Decl =
  Var of Id
| Proc0 of Id * (Comm list)   (* not used in this assignment; ignore it *)
| Proc of Id * (Id list) * (Comm list)

type Prog = (Decl list) * (Comm list)

exception SyntaxError of string * string list  (* use this as the error value *)


(* Here are functions that convert parse trees to strings for printing;
   Each function is defined like this:
      Tree2string : Tree -> string
*)
fun digit2string n = implode[chr(n + ord(#"0"))]

fun Int2string n = 
      let fun i2s n =   (* does base-10 arithmetic *)
                if n > 0 
                then (i2s (n div 10))^(digit2string(n mod 10))
                else ""
       in if n = 0
          then "0"
          else if n > 0
          then i2s n
          else "~"^(i2s (~n))
      end

fun Prog2string(ds, cs) =
    "( " ^ DeclList2string(ds) ^ ",  " ^ CommList2string(cs) ^ " )"

and DeclList2string ds = 
        let fun dl2s [] = ""
            |   dl2s (d::ds) = " " ^ Decl2string(d) ^ "," ^ dl2s(ds)
        in "[" ^ dl2s(ds) ^ "]"
        end

and Decl2string (Var(x)) = "Var(" ^ x ^ ")"
|   Decl2string (Proc0(x, cs)) = "Proc0(" ^ x ^ ", " ^ CommList2string(cs) ^ ")"
|   Decl2string (Proc(x, ps, cs)) = "Proc(" ^ x ^ ", " ^ IList2string(ps) ^ ", " ^ CommList2string(cs) ^ ")"

and IList2string is =
        let fun il2s [] = ""
            |   il2s (i::s) = " " ^ i ^ "," ^ il2s(s)
        in "[" ^ il2s(is) ^ "]"
        end

and CommList2string cs = 
        let fun cl2s [] = ""
            |   cl2s (c::cs) = " " ^ Comm2string(c) ^ "," ^ cl2s(cs)
        in "[" ^ cl2s(cs) ^ "]"
        end

and Comm2string (Assign(x,e)) = "Assign(" ^ x ^ ", " ^ Exp2string(e) ^ ")"
|   Comm2string (Print(e)) = "Print(" ^ Exp2string(e) ^ ")"
|   Comm2string (While(e,cs)) = "While(" ^ Exp2string(e) ^ ", " ^ CommList2string(cs) ^ ")"
|    Comm2string (Call0(x)) = "Call0(" ^ x ^ ")"
|    Comm2string (Call(x, es)) = "Call(" ^ x ^ ", " ^ ExprList2string(es) ^")"

and Exp2string (Num(n)) = "Num(" ^ Int2string(n) ^ ")"
|   Exp2string (L(x)) = "L(" ^ x ^ ")"
|   Exp2string (Add(e1, e2)) = "Add(" ^ Exp2string(e1) ^ ", " ^ Exp2string(e2) ^ ")"
|   Exp2string (Sub(e1, e2)) = "Sub(" ^ Exp2string(e1) ^ ", " ^ Exp2string(e2) ^ ")"

and ExprList2string es =
        let fun el2s [] = ""
            |   el2s (e::s) = " " ^ Exp2string(e) ^ "," ^ el2s(s)
        in "[" ^ el2s(es) ^ "]"
        end

fun StringList2string s =
        let fun sl2s [] = ""
            |   sl2s (e::s) = " " ^ e ^ "," ^ sl2s(s)
        in "[" ^ sl2s(s) ^ "]"
        end

;


(*******************************************************************
   Scanner: maps a string to a list of words, where each word is a string

   Example use:
    val words = scan("x = (2+1); call p(x)");
    words = ["x", "=", "(", "2", "+", "1", ")", ";", "call", "p", "(", "x", ")"]
*)

(* is_digit(ch)  returns whether  ch  is a digit *)
fun is_digit(ch) = ord(ch) >= ord(#"0") andalso ord(ch) <= ord(#"9")

(* is_letter(ch)  returns whether ch is a letter *)
fun is_letter(ch) = 
      (ord(ch) >= ord(#"a") andalso ord(ch) <= ord(#"z"))
         orelse
      (ord(ch) >= ord(#"A") andalso ord(ch) <= ord(#"Z"))

(* scanNum(inp)  reads some letters from char list  inp  and returns
   the numeral extracted along with the remaining  chars.

   scanId(inp)  reads some letters from char list  inp  and returns
   the word (identifier) extracted along with the remaining  chars.

   Both functions use a helper function,  scanToken   *)
fun scanToken(constraint, inp) =
      let fun scan0([],acc) = (acc,[]) 
          |   scan0(c::cs,acc) = 
                if constraint(c) 
                then scan0(cs, acc^str(c))
                else (acc,c::cs)
       in scan0(inp,"") 
      end
fun scanNum(inp) = scanToken(is_digit, inp)
fun scanId(inp) = scanToken(is_letter, inp)


(* separator characters and lookup function: *)
val separators = [#";", #"=", #"+", #"-", #"(", #")", #"{", #"}", #".", #":", #","]

fun member(ch, []) = false
|   member(ch, c::cs) = if ch = c 
                        then true
                        else member(ch, cs)
fun is_separator(c) = member(c, separators)


(* Finally, here is the scanner, which converts a string to a
   list of words (strings).  The typing is   scan: string -> string list *)
fun scan(textstring) =
let fun scanList [] = []     (* scan a list of chars *)
    |   scanList (c::cs) =
          if is_separator(c)
          then str(c) :: scanList(cs)
          else if is_digit(c)
          then let val (n,cs2) = scanNum(c::cs) 
               in n :: (scanList cs2) 
               end  
          else if is_letter(c)
          then let val (id,cs2) = scanId(c::cs)
               in id :: (scanList cs2)      
               end
          else (* the lead char, c,  is a blank or \n or trash;  skip it *)
               scanList cs
in scanList(explode textstring) end


(************************************************************************
  Parser:  maps a list of words (strings) to a parse tree.
  The main function is   parse :  string -> Prog

  Now, we have parsing functions, one for each datatype (grammar rule).
   Each function has the form,  
       parseX : string list ->  XTree * (string list)
   meaning that some strings are taken from the input arg, assembled
   into an  XTree value, and returned are the XTree and the remaining words *)

(* first, some helper functions that define keywords, numerals, identifiers: *)
val keywords = ["while", "call", "if", "else", "print", "int", "proc", "end"]

fun isKeyword(w) =
    let fun member(w, []) = false
    |       member(w, k::ks) = (w = k) orelse member(w,ks)
    in member(w, keywords)
    end

fun isNumeral(w) = 
    let fun is_digit(ch) = ord(ch) >= ord(#"0") andalso ord(ch) <= ord(#"9")
        fun isAllDigits([]) = true
        |   isAllDigits(d::ds) = is_digit(d) andalso isAllDigits(ds)
    in isAllDigits(explode w)
    end

fun isIden(w) = 
    let fun is_letter(ch) = 
             (ord(ch) >= ord(#"a") andalso ord(ch) <= ord(#"z"))
               orelse (ord(ch) >= ord(#"A") andalso ord(ch) <= ord(#"Z"))
        fun isAllLetters([]) = true
        |   isAllLetters(l::ls) = is_letter(l) andalso isAllLetters(ls)
    in isAllLetters(explode w) andalso not(isKeyword(w))
    end

(* converts a numeral string into an int:  *)
fun string2int(w) =
    let fun loop([], ans) = ans
        |   loop(d::ds, ans) =
                 let val n = ord(d) - ord(#"0") in
                 loop(ds, (10 * ans) + n)
                 end
    in loop(explode w, 0)
    end

 
(* EXPRESSION ::= NUMERAL  |  ID  |  ( EXPRESSION OPERATOR EXPRESSION )
   parseExp: string list -> Exp * string list 
*)
fun parseExp([]) = raise (SyntaxError ("expression expected", []))
|   parseExp(w::ws) =
      if isNumeral(w)
         then (Num(string2int(w)), ws)
      else if isIden(w)
         then (L(w), ws) 
      else if w = "("
         then let
              (* helper function to parse 2nd operand of binary expression: *)
              fun parseRest(opp, exp1, ws) =
                  let val (exp2, ws2) = parseExp(ws) in
                  if hd(ws2) = ")"
                  then (opp(exp1, exp2), tl(ws2))
                  else raise (SyntaxError ("bad expr syntax", ws))
                  end

              val (exp1, ws1) = parseExp(ws) 
              in
              if hd(ws1) = "+" then parseRest(Add, exp1, tl(ws1))
              else if hd(ws1) = "-" then parseRest(Sub, exp1, tl(ws1))
              else raise (SyntaxError("bad expr syntax", ws1))
              end
      else raise (SyntaxError ("bad expr syntax", w::ws))


(* ELIST ::= EXPRESSION,* 
   parseExpList : string list -> (Exp list) * string list 
*)
and parseExpList(w::ws) =
    if w = ":" orelse w = ")" 
    then ([], w::ws)
    else let val (e, ws1) = parseExp(w::ws) in
         if hd(ws1) = ","
         then let val (elist, ws2) = parseExpList(tl(ws1)) in
              (e :: elist, ws2) 
              end
         else ([e], ws1)
         end
;

(* COMMAND ::=  ID = EXPRESSSION
             |  print EXPRESSION
             |  while EXPRESSION : COMMANDLIST end
             |  call ID ( ELIST )
   parseComm: string list -> Comm * string list
*)
fun parseComm([]) = raise (SyntaxError("command expected", []))
|   parseComm(w::ws) =
        if isIden(w)   (* ID = EXPRESSSION *)
        then if hd(ws) = "="
             then let val (exp, ws1) = parseExp(tl(ws))
                  in  (Assign(w, exp), ws1)  end
             else raise (SyntaxError("bad assignment syntax --- missing keyword,  call ?", ws))
        else if w = "print"  (* print EXPRESSION *)
             then let val (exp, ws1) = parseExp(ws)
                  in  (Print(exp), ws1)  end
        else if w = "while"  (* while EXPRESSION : COMMANDLIST end *)
             then let val (exp, ws1) = parseExp(ws) in
                  if hd(ws1) = ":"
                  then let val (clist, ws2) = parseCommList(tl(ws1)) in
                       if hd(ws2) = "end"
                       then (While(exp, clist), tl(ws2))
                       else raise (SyntaxError("bad loop syntax",ws2))
                       end
                  else raise (SyntaxError ("bad loop syntax",ws1))
                  end
        else if  w = "call"  (* call ID { ( EXPLIST ) }  *)
             then if isIden(hd(ws))
                  then if hd(tl ws) = "("
                       then  (* parse "( EXPLIST )" *)
                            let val (elist, ws1) = parseExpList(tl(tl ws)) in
                                if hd(ws1) = ")"
                                then (Call(hd(ws), elist), tl ws1)
                                else raise (SyntaxError("missing ) in call",ws1))
                            end
                       else (Call0(hd(ws)), tl(ws))
                  else raise (SyntaxError("bad call syntax", ws))
        else raise (SyntaxError("command expected", w::ws))


(* COMMANDLIST ::=  COMMAND  |  COMMAND ; COMMANDLIST
   parseCommList: string list -> Comm list * string list
*)
(*and parseCommList(ws) =
    let val (cmd, ws1) = parseComm(ws) in
    if ws1 = [] then ([cmd], ws1)
    else if hd(ws1) = ";"
         then let val (clist, ws2) = parseCommList(tl(ws1))  in
              ([cmd] @ clist, ws2) end
    else ([cmd], ws1)
    end
;*)
and parseCommList(ws) =
        if ws = [] orelse hd(ws) = "end" 
        then ([], ws)
        else if hd(ws) = ";"
             then parseCommList(tl(ws)) 
        else let val (cmd, ws1) = parseComm(ws) in
             let val (clist, ws2) = parseCommList(ws1)  in
              ([cmd] @ clist, ws2) end end
;

(* ILIST ::=  ID,*
   parseIdList :  string list -> (ID list) * string list
*)
fun parseIdList(w::ws) =
    if w = ":" orelse w = ")" 
    then ([], w::ws)
    else if isIden(w)
         then if hd(ws) = ","
              then let val (ilist, ws1) = parseIdList(tl(ws)) in
                   (w :: ilist, ws1)  end
              else ([w], ws)
         else raise (SyntaxError("bad iden list syntax", w::ws))
;

(* DECLARATION ::=  int VAR  |  proc VAR : COMMANDLIST end
   parseDecl: string list -> Decl * string list
*)
fun parseDecl [] =  raise (SyntaxError("decl expected", []))
|   parseDecl(w::ws) =
        if w = "int"  (* int VAR *)
           then if isIden(hd(ws))
                then (Var(hd(ws)), tl(ws))
                else raise (SyntaxError("bad var decl syntax", ws))
        else if w = "proc"  (* proc ID { ( IDLIST ) } : COMMANDLIST end *)
            then if isIden(hd(ws)) andalso hd(tl ws) = "("
                 then  (* parse "( IDLIST )" *)
                       let val (ilist, ws1) = parseIdList(tl(tl ws)) in
                       if hd(ws1) = ")" andalso hd(tl ws1) = ":"
                          then let val (clist,ws2) = parseCommList(tl(tl(ws1))) in
                               if hd(ws2) = "end"
                               then (Proc(hd(ws), ilist, clist), tl(ws2))
                               else raise (SyntaxError("bad proc decl syntax", ws2))
                               end
                          else raise (SyntaxError("bad proc decl syntax", ws1))
                       end
                 else if isIden(hd(ws)) andalso hd(tl(ws)) = ":"
                      then let val (clist, ws1) = parseCommList(tl(tl(ws))) in
                           if hd(ws1) = "end"
                           then (Proc0(hd(ws), clist), tl(ws1))
                           else raise (SyntaxError("bad proc decl syntax", ws1))
                           end
                 else raise (SyntaxError("bad proc decl syntax", ws))
        else raise (SyntaxError("bad decl syntax", w::ws))

(* DECLIST ::=  DECLARATION ; DECLIST  |  (nothing)
   parseDeclList: string list -> Decl list * string list
*)
and parseDeclList([]) = ([], [])
|   parseDeclList(w::ws) =
    if w = "int" orelse w = "proc"
    then let val (dec, ws1) = parseDecl(w::ws) in
         if hd(ws1) = ";"
         then let val (dlist, ws2) = parseDeclList(tl(ws1))  in
              ([dec] @ dlist, ws2) end
         else raise (SyntaxError("semicolon expected after decl", ws1))
         end
    else ([], w::ws)
;

(* PROGRAM ::=  DECLIST COMMANDLIST 
   parseProg : string list -> Decl list * string list
*)
fun parseProg(ws) =
    let val (decls, ws1) = parseDeclList(ws)
        val (cmds, ws2) = parseCommList(ws1)
    in ((decls, cmds), ws2)
    end


(* Driver function:  parse : string list -> Prog   *)
fun parse(inputtext) =
    let val wordlist = scan(inputtext)
        val (tree, rest) = parseProg(wordlist)
    in  if not(rest = [])
        then raise (SyntaxError("input contains symbols after the program", rest))
        else tree
    end
    handle SyntaxError(message, words) => ( print (message^"\n");
                                            print ("Here are the words that remained when the error appeared:\n");
                                            print (StringList2string(words)^"\n");
                                            (nil, nil) )
