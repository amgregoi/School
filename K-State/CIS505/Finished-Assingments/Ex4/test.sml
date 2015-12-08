(* reverseloop(ns, ans)  reverses the items in list  ns  and appends them
    to the end of  ans.
   Precondition:  both  ns  and  ans  are lists.
   Postcondition: the returned answer is a list that holds the elements
     of  ans  followed by the elements of  ns  in reverse order.
   To use the function to reverse a list, x,  do this:  reverseloop(x, []).
*)
fun reverseloop(nil, ans) = ans
|   reverseloop(n::ns, ans) = reverseloop(ns, n :: ans)

(* reverse(ns)  reverses the items in list  ns.
   Precondition:  ns  is a list.
   Postcondition: the returned answer is a list that holds the elements
     of  ns  in reverse order.
*)
fun reverse (nil)  = []
|   reverse (n::ns) = (reverse ns) @ [n]