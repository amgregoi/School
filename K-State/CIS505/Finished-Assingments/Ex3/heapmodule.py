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

ns = []  # This is the handle to the namespace in the heap that holds the
         # program's global variables.  See  initializeHeap  below.


### Maintenance functions:


def activeNS():
    """returns the handle of the namespace that holds the currently visible
       program variables
    """
    global ns
    return ns[-1]


def initializeHeap():
    """resets the heap for a new program"""
    global heap_count, heap, ns
    heap_count = 0
    heap = {}
    ns.append(allocateNS())  # create namespace in  heap  for global variables


def printHeap():
    """prints contents of  ns  and  heap"""
    global heap
    print "activation stack = ['" + activeNS() + "']"
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
    heap[newloc] = {'parentns': 'nil'}
    heap_count = heap_count + 1
    ns.append(newloc)
    return newloc

def allocateClosure(ns, typ, rval, il, cl) :
    """helper function that allocates a closure for declaring procs/classes"""
    global heap_count, heap
    newloc = "h" + str(heap_count)
      
    if typ == 'proc' :
      heap[newloc] = [typ, il, cl, ns]
    elif typ == 'class' :
      heap[newloc] = [typ, cl, ns]

    declare(ns, rval, newloc)
    heap_count = heap_count + 1

def deallocateNS() :
    """deallocates the current namespace as long as it isn't the last one on the stack"""
    global ns, heap, heap_count
    if len(ns) != 1:
        namespace = ns.pop()

def isLValid(handle, field):
    """checks if  (handle, field)  is a valid L-value, that is, checks
       that  heap[handle]  is a namespace  and   field  is found in it.
       returns  True  if the above holds true; returns  False  otherwise.
    """
    return (handle in heap) and (field in heap[handle])


def lookup(handle, field) :
    """looks up the value of  (handle,field)  in the heap checks parent namespaces as necessary
       param: handle,field -- such that  isLValid(handle, field)
       returns: The function extracts the object at  heap[handle],
                indexes it with field,  and returns  (heap[handle])[field]
    """
    currhandle = handle
    while True:
        if isLValid(currhandle, field):
            return heap[currhandle][field]
        if heap[currhandle]['parentns'] == 'nil':
            crash("invalid lookup address: " + handle + " " + field)
        currhandle = heap[currhandle]['parentns']

def lookupheap(handle):
    """Lookup a heap by handle (for procedure calls)"""
    if handle not in heap:
        crash("invalid handle")
    return heap[handle]

def storeheap(handle, rval):
    """Store rval on the heap at handle (handle must exist)"""
    if handle not in heap:
        crash("invalid handle")
    heap[handle]  = rval


def declare(handle, field, rval) :
    """creates a new definition in the heap at (handle, field) and initializes
       it with rval, provided that  heap[handle][field] does not already exist!
       (else crashes with a "redeclaration error")

       params: handle, field, as described above
               rval -- an int or a handle
    """
    if field in heap[handle].keys(): #declare/store vars on heap
        crash("redeclaration error")
    heap[handle][field] = rval

def store(handle, field, rval) :
    """stores  rval  at heap[handle][field], provided that
         (i)  isLValid(handle,field)
         (ii) the type of  rval  matches the type of what's already stored at
              heap[handle][field]
        (iii) recursively checks parent namespaces for the variable declaration
       (else crashes)

       params:  handle, field, as described above
                rval -- an int or a handle
    """
    global heap
    currhandle = handle
    while True:
        if isLValid(currhandle, field):
            if type(heap[currhandle][field]) == type(rval):
                heap[currhandle][field] = rval
                break
            else:
                crash("field of wrong type")
        if heap[currhandle]['parentns'] == 'nil':
            crash("field not declared first")
        currhandle = heap[currhandle]['parentns']


def crash(message) :
    """prints message and stops execution"""
    print "Heap error: ", message, " Crash!"
    printHeap()
    raise Exception   # stops the interpreter
