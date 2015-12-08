
female('Carnival Woman').
male('Abraham Simpson').
female('Penelope Olsen').
male('Herbert Powell').
male('Homer Simpson').
male('Bart Simpson').
female('Lisa Simpson').
female('Maggie Simpson').
female('Marge Bouvier').
male('Clancy Bouvier').
female('Jacqueline Gurney').
female('Patricia Bouvier').
female('Selma Bouvier').

/* ...you do the remainder of the gender clauses;
   consult the above web link if you are unsure about any person's gender. */
female('Ling Bouvier').

/* predicate   parents(CHILD, FATHER, MOTHER)  asserts that 
   CHILD  has FATHER as its father and  MOTHER  as its mother:
*/

parents('Herbert Powell', 'Abraham Simpson', 'Carnival Woman').
parents('Homer Simpson', 'Abraham Simpson', 'Penelope Olsen').
parents('Bart Simpson', 'Homer Simpson', 'Marge Bouvier').
parents('Lisa Simpson', 'Homer Simpson', 'Marge Bouvier').
parents('Maggie Simpson', 'Homer Simpson', 'Marge Bouvier').
parents('Marge Bouvier', 'Clancy Bouvier', 'Jacqueline Gurney').
parents('Patricia Bouvier', 'Clancy Bouvier', 'Jacqueline Gurney').
parents('Selma Bouvier', 'Clancy Bouvier', 'Jacqueline Gurney').
/* ...you do the remainder of the parent clauses up to this last one: */
parents('Ling Bouvier', none, 'Selma Bouvier').
/* sister(X, Y)  defines that  X  has  Y as a sister if
   Y is female,  X's and Y's parents are the same,  and  X != Y  */
sister(X,Y) :- female(Y),
               parents(X,Father,Mother), parents(Y,Father,Mother),
               X \= Y.
/* aunt(X, A)  defines that  X  has  A  as an aunt */
aunt(X,A) :- parents(X, Y, Z), sister(Z, A).
aunt(X,A) :- parents(X, Y, Z), sister(Y, A).

/* uncle */
uncle(X,A) :- parents(X, Y, Z), brother(Z, A).
uncle(X,A) :- parents(X, Y, Z), brother(Y, A).

/* halfBrother(X, Y)  defines that  X and Y  are half brothers. */

halfBrother(X, Y) :- male(Y), parents(X, Father, Mother), parents(Y, Father, Z), X \= Y, not(brother(X, Y)).
halfBrother(X, Y) :- male(Y), parents(X, Father, Mother), parents(Y, Z, Mother), X \= Y, not(brother(X, Y)).

/* brother(X, Y)  defines that  X and Y  are brothers. */
brother(X, Y) :- male(Y), parents(X, Father, Mother), parents(Y, Father, Mother), X \= Y.


/* niece(X, Y)  defines that  X has Y as a niece.  */

niece(X, Y) :- female(Y), uncle(Y, X).
niece(X, Y) :- female(Y), aunt(Y, X).

/* nephew(X, Y)  defines that  X has Y as a nephew.  */

newphew(X, Y) :- male(Y), uncle(Y, X).
newphew(X, Y) :- malex(Y), aunt(Y, X).


