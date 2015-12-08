/* baby database with rollback implemented by prolog predicates,
         mapsto(Key, Value)   and    upd(Key, Value)  
   The predicates' assertions will be inserted by using  asserta :  
*/
:- dynamic mapsTo/2, upd/2.


/* clauses to build the committed database as a set of  mapsTo  clauses:  */
/* addDB(List)  holds true exactly when all the  (K,V)  pairs in  List
   are asserted as   mapsTo(K,V)  in the database   */
addDB([]).
addDB([(K,V)|Rest]) :- asserta(mapsTo(K,V)), addDB(Rest).

/*  lookup(K)  holds true when  K,V  is found in the database.  V  prints.  */
lookup(K) :- write('WRITE ME'), nl.

/* update(K,NewV)  holds true when  upd(K,NewV)  is asserted in the database */
update(K, NewV) :- asserta(upd(K,NewV)), write(K), write(' updated'), nl.
                   
/* revert  holds true when the most recently asserted  upd  is retracted. */
revert :- write('WRITE ME'), nl.

/* commit  holds true when:
    1.  one finds all the (K,V) pairs such that  upd(K,V)  holds true 
         and saves them in a list (HINT: use findall);
    2.  one retains only the most recent (visible) updates of the (K,V) pairs
         from the list in Step 1 (Hint: use  removedups  below).
    3.  one retracts all the  upd(K,_) and mapsTo(K,_) predicates
         for each (K,V)  retained in the list in Step 2.  (HINT: use  retractall)
    4.  one adds to the DB,  mapsTo(K,V),  for each (K,V) retained in  Step 2.
*/
commit :- write('WRITE ME'), nl.


/* removedups(L, M)  holds true when list  M  holds exactly the first (leftmost)
      occurrence of each (K,_) that is found in list L.   
   (Note:  select(I, L, M)  is a built-in Prolog predicate that holds true if it
           finds I in L and removes it, yielding M.)  */
removedups(L, M) :- nodups(L, M), !.
nodups([], []).
nodups([(K,V)|R], [(K,V)|T]) :- nodups(R, S), select((K,_), S, T).
nodups([(K,V)|R], [(K,V)|T]) :- nodups(R, T).

/*  This version avoids cut (!), but it is less nice to use at the console:
removedups([], []).
removedups([(K,V)|R], [(K,V)|T]) :- removedups(R, S), select((K,_), S, T).
removedups([(K,V)|R], [(K,V)|T]) :- removedups(R, T), notmember(K, T).
notmember(K, []).
notmember(K, [(KK,V)|T]) :- K \= KK,  notmember(K, T).
*/
