

###  HEAP-STORAGE MODULE

"""The program's heap is a dictionary that maps handles to namespaces.
   An object is itself a namespace (dictionary).

      heap : { (HANDLE : NAMESPACE)+ }
             where  HANDLE = a string of digits
                    NAMESPACE = a dictionary that maps var names to ints:
                                { (ID : INT)* }
   Example:
     heap = { "0": {"x":7, "y":1, "z":2} }
     heap_count = 1
        is an example heap, where handle "0" names a namespace
        whose  x  field holds int 7, "y" field holds int 1,
        and "z" holds int 2.

   The above example heap was generated from this sample program:
        int y = 1;  int x = (6 + y);  int z = y;
        z = (z + y)
"""

heap = {}

heap_count = 0  # how many objects stored in the heap

ns = ""  # This is the handle to the namespace in the heap that holds the
         # program's global variables.  See  initializeHeap  below.


### Maintenance functions:


def activeNS():
    """returns the handle of the namespace that holds the currently visible
       program variables
    """
    return ns


def initializeHeap():
    """resets the heap for a new program"""
    global heap_count, heap, ns
    #heap_count = 0
    #heap = {}
    ns = allocateNS()  # create namespace in  heap  for global variables


def printHeap(): 
    """prints contents of  ns  and  heap"""
    print "namespace =", ns

    print "heap = {"
    handles = heap.keys()
    handles.sort()
    for h in handles: 
        print " ", h, ":", heap[h]
    print "}"


def allocateNS() :
    """allocates a new, empty namespace in the heap and returns its handle"""
    global heap_count
    newloc = "h" + str(heap_count)  # generate handle of form,  hn,  where  n  is an int
    heap[newloc] = {}
    heap_count = heap_count + 1
    return newloc


def isLValid(handle, field):
    """checks if  (handle, field)  is a valid L-value, that is, checks
       that  heap[handle]  is a namespace  and   field  is found in it.
       returns  True  if the above holds true; returns  False  otherwise.
    """
    return (handle in heap) and (field in heap[handle])


def lookup(handle, field) :
    """looks up the value of  (handle,field)  in the heap
       param: handle,field -- such that  isLValid(handle, field)
       returns: The function extracts the object at  heap[handle],
                indexes it with field,  and returns  (heap[handle])[field]
    """
    if isLValid(handle, field) :
        return  heap[handle][field]
    else :
        crash("invalid lookup address: " + handle + " " + field)


def declare(handle, field, rval) :
    """creates a new definition in the heap at (handle, field) and initializes
       it with rval, provided that  heap[handle][field] does not already exist!
       (else crashes with a "redeclaration error")

       params: handle, field, as described above
               rval -- an int or a handle
    """
    ## WRITE ME:
    pass
    

def store(handle, field, rval) :
    """stores  rval  at heap[handle][field], provided that
         (i)  isLValid(handle,field)
         (ii) the type of  rval  matches the type of what's already stored at
              heap[handle][field]
       (else crashes with a type-error message)

       params:  handle, field, as described above
                rval -- an int or a handle
    """
    ## REVISE THE FOLLOWING CODE TO MATCH THE ABOVE DOCUMENTATION:
    heap[handle][field] = rval


def crash(message) :
    """prints message and stops execution"""
    print "Heap error: ", message, " Crash!"
    printHeap()
    raise Exception   # stops the interpreter
