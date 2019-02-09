#Normal Composition of two functions
def o(f,g):
    c = lambda x:f(g(x))
    return c

#iterated composition with self or list of composable maps
def comp(*functs,n=0):

    if n > 0 and type(n) is int: #self composition
        f_k = lambda x:x #f_0 should be identity function
        for i in range(n):
            f_k = o(functs[0],f_k) #f_k = f_0^k
        return f_k #return f^k = f^n = full composition

    else: #composition
        f_k = lambda x:x #f_0 should be identity function
        for f in reversed(functs):
            f_k = o(f,f_k) #f_k is k-th composition
        return f_k #return f_k = f_n = full composition
