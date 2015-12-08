/* Functor for defining book and dvd objects:
      ITEM ::=  book(TITLE, AUTHOR)  |  dvd(TITLE)
                     where TITLE and AUTHOR are strings

   Predicates that define ownership of an object
   and when an object is borrowed from the library:

      PRED ::=  owns(KEY, ITEM)  |  borrowed(KEY, PERSON, DUEDATE)
                    where KEY is an atom that begins with  k
                          ITEM is defined above
                          PERSON is an atom
                          DUEDATE is an int
*/
owns(k0, book('David Copperfied', 'Charles Dickens')).
owns(k1, book('Tale of Two Cities', 'Charles Dickens')).
owns(k2, book('Tale of Two Cities', 'Charles Dickens')).
owns(k3, dvd('Tale of Two Cities')).
owns(k4, book('Moby Dick', 'Herman Melville')).
owns(k5, dvd('Brothers Karamazov', 'Fyodor Dostoyevski')).

borrowed(k2, 'Homer', 10).
borrowed(k4, 'Homer', 20).
borrowed(k3, 'Lisa', 40).
borrowed(k0, 'Lisa', 45).
borrowed(k5, 'Homer', 90).

/* overdue  holds true when  ItemKey is borrowed (by  Who)  and is due earlier than  Today */
overdue(ItemKey, Today) :- borrowed(ItemKey, _, DueDate),
                           Today > DueDate.
						   
/* overdue  holds true when  ItemKey is borrowed (by  Who)  and is due earlier than  Today  -- incorporates Who*/
overdue(ItemKey, Today, Who) :- borrowed(ItemKey, Who, DueDate),
                           Today > DueDate.

/* fine  calculates the int value of  HowMuch  when  ItemKey  is overdue as of  Today */
fine(ItemKey, Today, HowMuch) :- overdue(ItemKey, Today),
                                 borrowed(ItemKey, _, DueDate),
                                 HowMuch is  Today - DueDate.

/* getBorrowed(Who, ItemList)  calculates a list of  KEYs
     of all the items  Who  has borrowed. */
getBorrowed(Who, ItemList) :- findall(Key, borrowed(Key, Who, _), ItemList).

/* getOverdue(Who, Today, ItemList)  calculates  ItemList,  which is a list of  KEYs
     of all the items  Who  has borrowed that are overdue as of  Today. */
	 
getOverdue(Who, Today, ItemList) :- findall(Key, overdue(Key, Today, Who), ItemList).

/* totalfine(Who, Today, Amount)  calculates  Amount,  which is an int
   that states the total fine that  Who  owes due to overdue items as of  Today */
totalfine(Who, Today, Amount) :- findall(HowMuch, (borrowed(Key, Who, _), fine(Key, Today, HowMuch)),List), test(List, Amount).

test([], 0).
test([H|Rest],Total) :- test(Rest, TotalOfRest), Total is H + TotalOfRest.






								 
								 
