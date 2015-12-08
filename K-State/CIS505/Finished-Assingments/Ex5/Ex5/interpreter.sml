(* INTERPRETER FOR MINI-C LANGUAGE  *)

(* The Interpret function assumes a "parse" function, written in  parser.sml,
   which defines these forms of parse tree:

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
| Call of Id * (Exp list)

and Decl =
  Var of Id
| Proc of Id * (Id list) * (Comm list)

type Prog = (Decl list) * (Comm list)
;

If we used the SML modules language, the above code would become for us
an _interface type_ for the interpreter.  Maybe later....
*)

(* EXCEPTIONS (error messages) *)
exception EnvLookupError
exception StoreFetchError
exception StoreError
exception RevertError
exception ProcReferenced of string
exception IntCalled of string
exception CallParamError
;

(* STRING-CONVERSION FUNCTION FOR INTs *)
fun digit2string n = implode[chr(n + ord(#"0"))]
fun int2string n = 
      let fun i2s n =
                if n > 0 
                then (i2s (n div 10))^(digit2string(n mod 10))
                else ""
       in if n = 0
          then "0"
          else if n > 0
          then i2s n
          else "~"^(i2s (~n))
      end
;

(********* ENVIRONMENT: defines denotable values and enviromnent 
    A denotable value is an int loc or a closure.
    An environment is a list of  name, denotable-value  pairs.
    Example:  val env0 = [ ("y", Loc(1)),
                           ("x", Loc(0))
                         ]
              val env1 = ("p", Closure(["a","b"], [Assign("x", Add(L("x"), L("y")))], env0)  ::  env0

            Now,  env1  holds bindings for proc  p  and vars  y and x.
            Notice how  p's closure holds (a link to)  env0.

    ML has a  _module_  construction, and the coding of the environment can/should be placed
    in its own module file.  Maybe later....
**********)

datatype Denotable = Loc of int  
                  |  Closure of (Id list)* (Comm list) * ((Id * Denotable) list)
                     (* NOTE:  See the next line!  *)
type Env = (Id * Denotable) list
;

(* string-conversion functions:  Denotable2string : Denotable -> string 
                                 Env2string : Env -> string
*)
fun Denotable2string (Loc(v)) = "Loc(" ^ int2string(v) ^ ")"
|   Denotable2string (Closure(params, body, link)) =
        "Closure(params:" ^ IList2string(params) ^ ", body:" ^ CommList2string(body)
         ^ ", linkto:"   ^ Env22string(link) ^ ")" 
and Env22string nil = "nil"
|   Env22string ((i,d)::t) =  "("^ i ^ ", " ^ Denotable2string(d) ^ ") :: " ^ (Env22string t)
;

fun Env2string nil = "nil"
|   Env2string ((i,d)::t) =  "("^ i ^ ", " ^ Denotable2string(d) ^ ")\n:: " ^ (Env2string t)
;


(* starting env: *)
val emptyenv : Env = nil
;

(* lookup(x, env)  searches for  x  in  env  and returns the denotable value
   paired with it,  e.g.,
     lookup("b",  Binding("a", Loc(0), Binding("b", Loc(1), Empty)))  returns  Loc(1).
   Raises  EnvLookupError  when  x  is not found in  env.
      lookup : string * Env -> Denotable
*)
fun lookup(x, []) = raise EnvLookupError
(*|	lookup(x, Binding(ch, loc, env)) = if x = ch then loc else lookup(x, Env) *)
|	lookup(x, ((ch, loc)::env)) = if x = ch then loc else lookup(x, env)

;

(* declare(x, d, env)  returns an Env that has (x,d) attached to env.
     declare: string * Denotable * Env -> Env
*)
fun declare(x, d, env: Env) = ((x,d)::env)
;


(*************** STORE: defines linear storage as a list of cells that hold ints 
                        Should be placed in its own module, someday....          
****************)

type Store = int list

(* string-conversion function for printing a store:  *)
fun Store2string (mem: Store) =
    let fun s2s [] = ""
        |   s2s (v::s) =  int2string(v) ^ ", " ^ (s2s s)
    in
    "[ " ^ (s2s mem) ^ "]"
    end

(* initial, empty store value: *)
val emptystore: Store = []
;

(* allocCell mem   builds a store that is  mem   extended by a new cell,
    initialized to 0, e.g.,   allocCell [4,5,7]  returns the pair,
      (3, [4,5,7,0])   namely, the new location and the updated store
        allocCell : Store -> (int * Store)
    NOTE: in ML, a pair is written like in Python, e.g., (3, []) 
*)
fun allocCell(mem : Store) = (length(mem), mem @ [0])
;
       
(* fetch(i, mem)   looks up and returns the int saved in location/position  i
     in  mem,  e.g.,  fetch(2, [4,5,7,9])  returns  7
   Raises  StoreFetchError  if location  i  not found in  mem
    fetch : int * Store -> int
*)
fun fetch(i, nil:Store) = raise StoreFetchError
|	fetch(i, (hd::tl):Store) = if i = 0 then hd else fetch(i-1, tl)
;

(* store(i, v, mem)  returns a store that looks like  mem  with the int
     at location  i  replaced by  v.  E.g.,
       store(1, 4, [3,5,7,9])  returns  [3,4,7,9]
   Raises  StoreError  if  location  i  not found in  mem
    store : int * int * Store -> Store
*)
fun store(i, v, nil: Store) = raise StoreError  (* WRITE ME *)
|	store(i, v, (hd::tl) : Store) : Store = if i = 0 then [v] @ tl else [hd] @ store(i-1, v, tl)
;

(* revert(i, mem)  returns a store that is  mem  shortened to length  i,
    e.g.,   revert(2, [3,5,7,9])  returns  [3,5].
   Raises  RevertError  if  i > length(mem).
   NOTE:  in ML,  length(mem)  returns the int length of list  mem.
     revert : int * Store -> Store
*)
fun revert(i, mem: Store) = if i > length(mem) then raise RevertError else if length(mem) = i then nil else [hd(mem)] @ revert(i, tl(mem))   (* WRITE ME *)
;


(*********** INTERPRETATION FUNCTIONS 
   All functions have form,
     interpretTree : Tree -> Env -> Store -> Answer
   where  Tree  is one of the datatypes documented at the top of this file.
   Notice that the arguments are "curried", that is, supplied one at a time,
   e.g.,  (interpretTree tree env mem)
   This style is exploited if we would add "higher-order constructions" to the
   programming language.

   The body of each  interpretTree  is written as one pattern equation for each
   form of parse Tree.
***************************)
   
(* interpretExp : Exp -> Env -> Store -> Int *)
fun interpretExp (Num(n)) env mem = n
|   interpretExp (L(id)) env mem  = 
        (case lookup(id, env) of
            Loc v => fetch(v, mem)
        |   Closure c => raise (ProcReferenced id)
        )
|   interpretExp (Add(e1, e2)) env mem =
        (interpretExp e1 env mem) + (interpretExp e2 env mem)
|   interpretExp (Sub(e1, e2)) env mem =
        (interpretExp e1 env mem) - (interpretExp e2 env mem)
;

(* interpretExpList : Exp list -> Env -> Store -> Int list 
	tree @ List
*)
fun interpretExpList nil env mem = nil
|	interpretExpList (tree::elist) env mem = [(interpretExp tree env mem)] @ (interpretExpList(elist) env mem)
;           

(* dec(ilist, elist, env, mem *)


(* interpretComm : Comm -> Env -> Store -> Store 
	based on the second function of interpretExp - hope this is what you were looking for?
*)
fun interpretComm (Assign(id, e)) env mem = 
		(case lookup(id, env) of
            Loc v => store(v, interpretExp e env mem, mem)
        |   Closure c => raise (ProcReferenced id)
        )

|   interpretComm (Print(e)) env mem = let val v = interpretExp e env mem  in 
                                       (print ((int2string v)^"\n");
                                        mem   (* return mem unaltered *)
                                       )
                                       end

|   interpretComm (While(e, clist)) env mem =
        let val v = interpretExp e env mem  in
        if not(v = 0)
           then interpretComm (While(e, clist)) env (interpretCommList clist env mem)
           else mem  (* loop finished, return existing store *)
        end
				
|   interpretComm (Call(id, elist)) env mem = 
        (print "WRITE THE CODE FOR A CALL\n";
			nil
		)
       
	   (*
	   (case lookup(id, env) of
              Closure(ilist, clist, cenv) => (
                let val oldlen = length mem 
					let fun dec((i::il), (e::el), (env : Env), (mem : Store)) : (Env * Store) = 
						let val (env0, mem0) = (interpretDecl (Var(i)) env mem) in
							let val newmem = interpretComm (Assign(i, e)) env0 mem0 in
							dec(il, el, envm, memn)
							end
						end
						|	dec(nil, nil, (env : Env), (mem : Store)) : (Env * Store) = (env,  mem)
						let val (envl, meml) = dec(ilist, elist, env, mem) in
							revert(oldlen, interpretCommList clist envl meml)
						end
				mem
                
               )
            | Loc v => raise(ProcReferenced id) *)


(* interpretCommList : Comm list -> Env -> Store -> Store *)
and interpretCommList clist env mem =
      let fun interpcomms [] e m = m
          |   interpcomms (c::cs) e m =  interpcomms cs e (interpretComm c e m)
      in let val exitmem = interpcomms clist env mem in
        (print "Finished commandlist: ";
         print (CommList2string clist);  print "\n";
         print "using env = \n";
         print (Env2string env); print "\n";
         print "Current store = \n";
         print (Store2string exitmem);  print "\n";
         exitmem
        ) 
      end end

(*THIS IS THE VERSION OF  interpretCommList  THAT DOES NOT PRINT DIAGNOSTICS:
and interpretCommList [] env s = s
|   interpretCommList (c::rest) env s =
                   interpretCommList rest env (interpretComm c env s)
*)
;

(* interpretDecl : Decl -> Env -> Store -> (Env * Store) *)
fun interpretDecl (Var(id)) env mem =
        let val (newloc, newmem) = allocCell mem 
            val newenv = declare(id, Loc(newloc), env)
        in (newenv, newmem)
        end 
|   interpretDecl (Proc(id, params, body)) env mem =
        let val (newloc, newmem) = allocCell mem
			val newenv = declare(id, Closure(params, body, env), env) (*Closure(parameters, Body of Proc, env)*)
		in (newenv, newmem)
		end
;

(* interpretDeclList : Decl list -> Env -> Store -> Store *)
fun interpretDeclList [] env mem = (env, mem)
|   interpretDeclList (d::rest) env mem =
         let val (newenv, newstore) = interpretDecl d env mem
         in  interpretDeclList rest newenv newstore
         end
;
 
(* MAIN FUNCTIONS: interpret: Prog -> Store *)
fun interpret (dlist, clist)  =
              let val (startenv, startstore) = interpretDeclList dlist emptyenv emptystore
              in
              interpretCommList clist startenv startstore
              end
