
/* baby database with rollback implemented as a hybrid ordered tree structure:

   DB ::=  upd(Key, Value, DB)  |  node(Key, Value, DB, DB)  |  leaf
   Key ::=  double-quoted character
   Value ::=  int 
*/

/* clauses that define the operations on a database:  */

/* lookup(K, DB, V)  holds true if (K,V) is found in database  DB by
      using an ordered-binary-tree lookup, like in Q3, Ex4.  */
lookup(K, DB, V) :- write('WRITE CLAUSES TO IMPLEMENT ME.'), nl.
                    /* HINT: study  insert,  below  */


/* update(K,V, DB, NewDB)  holds true if  NewDB  has (K,V) as its leading,
      updated value on the front of DB.  */
update(K,V,DB, upd(K, V, DB)).

/* revert(DB, OldDB) holds if  OldDB  is  DB  without its most recent update */
revert(upd(_,_, OldDB), OldDB).


/*  collect(DB, L)  holds true if  L  is a list of all the visible (K,V)
       pairs that are saved in DB.  (That is, the older, duplicate  (K,_)
       pairs are forgotten.)
*/
collect(DB, L) :-  write('WRITE CLAUSES TO IMPLEMENT ME.'), nl,
                   write('DONT FORGET TO REMOVE DUPLICATE KEYS.'), nl.
         /* HINT: code it like you did in Exercise 4, but in Prolog clauses.
                   Use Prolog's  append  operator to assemble lists.  */


/* clauses that construct the starting ordered DB tree: */

/* build(L, DB)  holds true if  DB  is a database value that holds all the
     (K,V)  pairs in list L  */
build([], leaf).
build([(K,V)|Rest], Ans) :-  build(Rest, Ans1), insert(K,V,Ans1,Ans).

/*  insert(K,V, DB, Ans)   holds true if ordered tree  Ans  consists of
    ordered tree DB  with (K,V)  inserted therein:  */
insert(K,V, leaf, node(K,V, leaf, leaf)).

insert(K,V, node(M,U, Left, Right), node(M,U, Newleft, Right))
                             :- K =< M, insert(K,V, Left, Newleft).

insert(K,V, node(M,U, Left, Right), node(M,U, Left, Newright))
                             :- K > M, insert(K,V, Right, Newright).



/* driver:  Datalist is a list of  (K,V) pairs. */
run(Datalist) :-  build(Datalist, DB),
                  write(DB), nl,
                  loop(DB).

/* loop is the control loop that reads and executes commands:  */
loop(DB) :- readCommand(C), execute(C, DB), !.

readCommand(Ans) :- write('Command? '), read(Ch), parse(Ch, Ans), nl.
parse('q', 'quit').
parse('r', 'revert').
parse('c', 'commit').
parse('l', ('lookup', K)) :- write('Key (double quoted)? '), read(K).
parse('u', ('update', K, V)) :- write('Key (double quoted)? '), read(K),
                                write('Value? '), read(V).

execute('quit', DB) :- collect(DB, L), printPairList(L).

execute(('lookup',K), DB) :- lookup(K, DB, V),
                             write(V), nl,
                             loop(DB).
/* use this clause if the previous clause fails: */
execute(('lookup',K), DB) :- write('lookup error'), nl, loop(DB).

execute(('update',K,V), DB) :-  update(K, V, DB, NewDB),
                                write(NewDB), nl,
                                loop(NewDB).

execute('revert', DB) :- revert(DB, NewDB),
                         write(NewDB), nl,
                         loop(NewDB).
/* use this clause if the previous clause fails: */
execute('revert',DB) :- write('revert error'), nl, loop(DB).

execute('commit', DB) :- collect(DB, Contents),
                         printPairList(Contents),
                         build(Contents, NewDB),
                         write(NewDB), nl,
                         loop(NewDB).

/* printPairList(L)  prints the (K,V) pairs in list  L.  */
printPairList([]) :- nl.
printPairList([(K,V)|Rest]) :- write('('), put(K), write(', '),
                               write(V), write('), '),
                               printPairList(Rest).

