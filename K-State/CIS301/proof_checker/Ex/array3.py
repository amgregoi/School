
"""{ def  sum(0) == 0
     def  sum(n+1) == sum(n) + a[n]
}"""


def add(a) :
    """{ pre  len(a) >= 0
         post answer == sum(len(a))
         return answer
    }"""
    answer = 0
    """{ 1. answer == 0     premise
         2. sum(0) == 0     def
         3. answer == sum(0)  algebra 1 2
    }"""
    i = 0
    while i != len(a) :
        """{ invariant  answer == sum(i)
             modifies answer, i           }"""
        """{ 1. answer == sum(i)    premise }"""
        answer = answer + a[i]
        """{ 1. answer == answer_old + a[i]   premise
             2. answer_old == sum(i)          premise
             3. answer == sum(i) + a[i]       subst 2 1
             4. sum(i+1) == sum(i) + a[i]     def
             5. answer == sum(i+1)            subst 4 3
        }"""
        i = i + 1
        """{ 1. answer == sum(i_old +1)     premise
             2. i == i_old + 1              premise
             3. answer == sum(i)            subst 2 1
        }"""

    """{ 1. answer == sum(i)        premise
         2. not(i != len(a))        premise
         3. i == len(a)             algebra 2
         4. answer == sum(len(a))   subst 3 1
    }"""
    return answer
    
