(* insert(m, ns)  inserts  m  in the correct position within list  ns.
   Precondition:  m  is an int  and  ns  is a sorted list of ints.
   Postcondition:  the returned answer is a sorted list containing exactly
      m  and the elements in  ns.
   Example:  insert(3, [2,4]) returns [2,3,4].
*)
fun insert(m, nil) = [m]
  | insert(m, n::ns) = if m < n then [m] @ [n] @ ns else [n] @ insert(m, ns);

(* isortloop(ns, ans)  calls  insert  to insert the elements of  ns  into  ans.
   Precondition:  ns  is a list of ints and  ans  is a sorted list of ints
   Postcondition: the answer returned is a sorted list of ints containing
     exactly the elements of  ns   and  ans.
   Call it like this:   isortloop(ns, []),
        e.g.,   isortloop([4,2,3,5,1], [])  returns  [1,2,3,4,5]
*)
fun isortloop(nil, ans) = ans
  |	isortloop((head::tail), ans) = isortloop(tail, insert(head, ans));

(* isort(ns)  calls  insert  to sort  ns.
   Precondition:  ns  is a list of ints
   Postcondition:  the answer returned is a sorted list of ints containing
     exactly the elements of  ns.
   Example:  isort([4,2,3,5,1])  returns  [1,2,3,4,5]
*)
fun isort(nil) = nil
  | isort(n::ns) = insert(n, isort(ns));