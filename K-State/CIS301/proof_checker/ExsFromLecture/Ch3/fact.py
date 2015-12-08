
def fact(n) :          
    """{ pre  n >= 0  
       post   ans = n!
       return  ans  
    }"""
    print "computing fac", n
    if n == 0 :
        ans = 1        # this computes  0! = 1
    else :
        a = fact(n-1)  # this computes  (n-1)!
        ans = a * n    # this computes  n! = (n-1)! * n
    print "finished computing fac", n, "=", ans
    return ans

