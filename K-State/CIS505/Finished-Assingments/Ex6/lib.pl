
/* Functors for defining book and dvd objects:

ITEM ::=  book(TITLE, AUTHOR)  |  dvd(TITLE)
             where TITLE and AUTHOR are atoms (single-quoted strings)

Predicates for defining library's ownership of an object
and for defining when an object is borrowed from the library:

PRED ::=  owns(KEY, ITEM)  |  borrowed(KEY, PERSON, DATE)

             where KEY is an atom that begins with  k
                   ITEM is defined above
                   PERSON is an atom
                   DATE is an int
*/

/* owns(KEY, ITEM)  defines that the library owns the ITEM and has
     labelled it with key  KEY  */
owns(k0, book('David Copperfied', 'Charles Dickens')).
owns(k1, book('Tale of Two Cities', 'Charles Dickens')).
owns(k2, book('Tale of Two Cities', 'Charles Dickens')).
owns(k3, dvd('Tale of Two Cities')).
owns(k4, book('Moby Dick', 'Herman Melville')).

/* borrowed(KEY, NAME, DUEDATE)  defines that  NAME  has borrowed the
    item whose key is KEY and with due date DUEDATE.  */
borrowed(k2, 'Homer', 44).
borrowed(k4, 'Homer', 46).
borrowed(k3, 'Lisa', 92).
borrowed(k0, 'Lisa', 92).

     
/* isOverdue  holds true if the  Item  borrowed by  Person  has a due date
   that is earlier than  Today.  */
isOverdue(Person, Item, Today) :- borrowed(Item, Person, DueDate), 
                                  Today > DueDate.


/* fineOf  is a "function" that calculates  HowMuch  the fine is,
     as of  Today,  for an overdue  Item.  */
fineOf(Item, Today, HowMuch) :- isOverdue(_, Item, Today),
                                borrowed(Item, _, DueDate),
                                HowMuch is  Today - DueDate .


/* TRY THIS:  ?- findall(ItemKey, borrowed(ItemKey, 'Homer', _), Ans).  */
printOverdue(Today) :- findall(Key, isOverdue(_, Key, Today), Ans), printTitles(Ans).

/* printBorrowed(Name)  prints the titles of all items borrowed by  Name */
printBorrowed(Name) :- findall(ItemKey, borrowed(ItemKey, Name, _), KeyList),
                       write('list of keys is '), write(KeyList), nl,
                       printTitles(KeyList).

/* printTitles(KeyList)  looks up the items named by the keys in  Keylist
      and prints the title of each item.  */
printTitles([]).
printTitles([H|Rest]) :- printTitle(H), nl, printTitles(Rest).

printTitle(Key) :- owns(Key, book(Title,_)), write(Title).
printTitle(Key) :- owns(Key, dvd(Title)), write(Title).


/* hasFine(Who, Today, Howmuch)  holds true when  Who  has borrowed items
     that are overdue as of Today, and the total fine of all the overdue 
     items is  Howmuch.
*/
hasFine(Who, Today, Howmuch) :- findall(X, (borrowed(Key, Who, _), fineOf(Key, Today, X)),List), sum(List, Howmuch).

/* sum(L, T)  holds true when  T  is the sum of all the ints in list  L.  */
sum([], 0).
sum([N|Rest], Total) :- sum(Rest, M),  Total is N + M.


 
