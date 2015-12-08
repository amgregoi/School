
# A bank account and its maintenance functions.
### A MODULE/CLASS THAT MODELS A BANK ACCOUNT ###############

# The global variable, the money in the account:
account = 100       # we'll start at 100....
# the global invariant (sometimes called the _class invarian_):
"""{ globalinv  account >= 0  }"""  # this property must stay true forever

def deposit(howmuch) :
    """deposit adds  howmuch  to  account"""
    """{ pre  howmuch >= 0    
         post  True }"""
    global account
    """{ 1.  account >= 0    premise # the globalinv holds on entry
         2.  howmuch >= 0    premise  # the function's precondition
         3.  account >= 0 and howmuch >= 0  andi 1 2
    }"""
    account = account + howmuch
    """{ 1. account == account_old + howmuch    premise
         2. account_old >= 0  and  howmuch >= 0    premise 
         3. account >= 0                         algebra 1 2
    }"""
    # We must prove the global invariant is preserved at the exit.

def withdraw(howmuch) :
    """withdraw  removes  howmuch  from  account"""
    """{ pre  howmuch >= 0      
         post  True }""" 
    global account
    # the same two premises hold here like in  deposit
    if  howmuch <= account :
        # now we know that  howmuch <= account :
        account = account - howmuch
        """{ 1. account == account_old - howmuch    premise
             2.  howmuch <= account_old            premise
             3.  account >= 0                     algebra 1 2
        }"""
    else :
        """{ 1. not(howmuch <= account)     premise
             2.  account >= 0               premise  # the invariant
        }"""
        pass
        """{ 1. account >= 0                premise }"""
    # END IF
    """{ 1. account >= 0                     premise }"""
    # The global invariant is preserved at the exit.

