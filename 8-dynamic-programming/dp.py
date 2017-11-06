def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def fib_cache(n):
    f = [None for i in range(n+1)]
    f[0] = 0
    f[1] = 1

    def fib(m):
        if f[m] is None:
            f[m] = fib(m-1) + fib(m-2)
        return f[m]

    return fib(n)

def fib_dp(n):
    f = [None for i in range(n+1)]
    f[0] = 0
    f[1] = 1
    for i in range(2, n+1):
        f[i] = f[i-1] + f[i-2]
    return f[n]

def fib_ultimate(n):
    assert n>=0
    if n < 2:
        return n
    back2, back1 = 0, 1

    for i in range(2, n+1):
        nxt = back1 + back2
        back2 = back1
        back1 = nxt
    return nxt

def binomial(n, m):
    p = [[0 for i in range(max(m,n) + 1)] for j in range(max(n,m) + 1)]
    for i in range(n+1):
        p[i][0] = 1
    for j in range(n+1):
        p[j][j] = 1
    for i in range(1, n + 1):
        for j in range(1, i):
            p[i][j] = p[i - 1][j - 1] + p[i - 1][j]
    return p[n][m]
