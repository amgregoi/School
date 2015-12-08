
g = [0,0]
def f() :
    """{ pre len(g) == 2  post g[0] == g_in[0] + 1 return ans }"""
    global g
    g[0] = g[0] + 1
    """{ 1. g[0] == g_old[0] + 1    premise
         4. g_old == g_in           algebra
         2. g_old[0] == g_in[0]    algebra
         5. g_old[0] == g_old[0]   algebra
         6. g_old[0] == g_in[0]    subst 4 5
         3. g[0] == g_in[0] + 1     subst 6 1
    }"""
    return ans

#x = f()
