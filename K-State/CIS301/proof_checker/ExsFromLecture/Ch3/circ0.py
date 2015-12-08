
pi = 3  # sorry --- the checker handles  ints  only  )-:

# a read-only global variable acts like an extra parameter:
def circ(diameter) :
    """{ pre  diameter >= 0  and  pi >= 3
         post  answer == pi * diameter  
         return answer
    }"""
    answer = pi * diameter
    return answer


"""{ 1. pi == 3   premise 
     2. pi >= 3   algebra 1
}"""
x = circ(2)
"""{ 1.  x == pi * 2   premise }"""

