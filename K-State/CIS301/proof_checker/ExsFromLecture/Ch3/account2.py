
### A MODULE/CLASS THAT MODELS A BANK ACCOUNT ###############

# The global variable, the money in the account:
account = 100       # we'll start at 1d0....
# the global invariant (sometimes called the _class invariant_):
"""{ globalinv  account >= 0  }"""  # this property must stay true forever

# A real account maintains a log of all the transactions:
log = [0+100]    # log  is an array (list) that grows.  Here, it has one entry.

# There is another global invariant: the  balance  is correct!
###  """{ globalinv   account == summation of  i: 0..log(len-1), log[i] }"""

# We can use  def  clauses, explained in Chapter 3, and arrays,
# explained in Chapter 6, to state and prove this property.


def deposit(howmuch) :
    """deposit adds  howmuch  to  account"""
    """{ pre  howmuch >= 0 
         post  True }"""
    global account, log
    """{ 1.  account >= 0    premise # the globalinv holds on entry
         2.  howmuch >= 0    premise  # the function's precondition
         3.  account >= 0 and howmuch >= 0  andi 1 2
    }"""
    account = account + howmuch
    """{ 1. account == account_old + howmuch    premise
         2. account_old >= 0  and  howmuch >= 0    premise 
         3. account >= 0                         algebra 1 2
    }"""
    log.append(0+howmuch)   # record the transaction in the log

    # We must prove the global invariants are preserved at the exit.


def withdraw(howmuch) :
    """withdraw  removes  howmuch  from  account"""
    """{ pre  howmuch >= 0 
         post  True }""" 
    global account, log
    # the same premises hold here like in  deposit
    if  howmuch <= account :
        # now we know that  howmuch <= account :
        account = account - howmuch
        """{ 1. account == account_old - howmuch    premise
             2.  howmuch <= account_old            premise
             3.  account >= 0                     algebra 1 2
        }"""
        log.append(0-howmuch)  # record the transaction in the log

    else :
        """{ 1. not(howmuch <= account)     premise
             2.  account >= 0               premise  # the invariant
        }"""
        pass
        """{ 1. account >= 0                premise }"""
    # END IF
    """{ 1. account >= 0                     premise }"""
    # We reprove the global invariants here.

