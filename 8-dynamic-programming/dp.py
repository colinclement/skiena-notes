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

def match(s, t):
    return 1 - (s == t)

def indel(s):
    """ if there is a space, either an insertion or deletion is required """
    return 1

def string_compare(s, t, i, j):
    if i < 0:  # no more of P to match
        return j * indel(" ")
    if j < 0:  # no more of T to edit
        return i * indel(" ")

    matched = edit_distance(s, t, i-1, j-1) + match(s[i], t[j])
    insert = edit_distance(s, t, i, j-1) + indel(t[j])
    delete = edit_distance(s, t, i-1, j) + indel(s[i])

    return min(matched, insert, delete)

from collections import namedtuple

Cell = namedtuple('Cell', ['cost', 'parent'])


class EditDistance(object):
    def match(self, s, t):
        return 1 - (s == t)
    
    def indel(self, s):
        """ if there is a space, either an insertion or deletion is required """
        return 1

    def row_init(self, i, m):
        for i in range(len(m)):
            m[i][0] = Cell(i, -1 if not i else 2)  # all deletes
    
    def col_init(self, j, m):
        for j in range(len(m[0])):
            m[0][j] = Cell(j, -1 if not j else 1)  # all inserts

    def goal_cell(self, s, t, m):
        return len(s) - 1, len(t) - 1

    def string_compare(self, s, t):
        if not s[0] == " ":
            s = " " + s
        if not t[0] == " ":
            t = " " + t
        
        maxlen = len(s) + len(t)
        m = [[None for i in range(len(t))] for j in
             range(len(s))]
        opt = [maxlen] * 3
        # Set boundary conditions, matching empty string
        self.row_init(i, m)
        self.col_init(j, m)
    
        for i in range(1, len(s)):
            for j in range(1, len(t)):
                opt[0] = m[i - 1][j - 1].cost + self.match(s[i], t[j])
                opt[1] = m[i][j - 1].cost + self.indel(t[j])
                opt[2] = m[i - 1][j].cost + self.indel(s[i])
    
                argsort = sorted(range(3), key = lambda i: opt[i])
                m[i][j] = Cell(opt[argsort[0]], argsort[0])
        
        i, j = self.goal_cell(s, t, m)
        return m[i][j].cost, m
    
    @staticmethod
    def match_out(s, t, i, j, path):
        if s[i] == t[j]:
            path.append("M")
        else:
            path.append("S")
   
    @staticmethod
    def insert_out(t, j, path):
        path.append("I")
    
    @staticmethod
    def delete_out(s, i, path):
        path.append("D")
    
    @staticmethod
    def reconstruct_path(m, s, t, i, j, path):
        if m[i][j].parent < 0:
            return
        if m[i][j].parent == 0:  # parent matched
            EditDistance.reconstruct_path(m, s, t, i - 1, j - 1, path)
            EditDistance.match_out(s, t, i-1, j-1, path)
            return
        if m[i][j].parent == 1:  # parent inserted
            EditDistance.reconstruct_path(m, s, t, i, j - 1, path)
            EditDistance.insert_out(t, j-1, path)
            return
        if m[i][j].parent == 2:  # parent deleted
            EditDistance.reconstruct_path(m, s, t, i - 1, j, path)
            EditDistance.delete_out(s, i-1, path)
            return


class SubstringMatch(EditDistance):
    def col_init(self, j, m):
        """ Don't penalize deleting a bunch of T to find close s """ 
        for j in range(len(m[0])):
            m[0][j] = Cell(0, -1)

    def goal_cell(self, s, t, m):
        """ Find part of m for full match of s and best match of t """
        i = len(s) - 1
        j =  sorted(range(len(m[0])), key=lambda j: m[i][j].cost)[0]
        return i, j


class LargestCommonSubsequence(EditDistance):
    def match(self, s, t):
        """ Substitute must be more costly than delete+insert """
        return 3 * (not s == t)


def reconstruct_partition(s, d, n, k, part):
    if k == 1:
        part.append(s[1:n+1])
    else:
        reconstruct_partition(s, d, d[n][k], k-1, part)
        part.append(s[d[n][k]+1:n+1])

def partition(s, k):
    """ partition integer array into most equitable k-partitions """
    s = [0] + s
    tot = sum(s)
    m = [[0 for j in range(k+1)] for i in range(len(s))]
    d = [[-1 for j in range(k+1)] for i in range(len(s))]
    for i in range(1,len(s)):
        m[i][1] = m[i-1][1] + s[i]  # one range is simply sum
    for j in range(1,k+1):
        m[1][j] = s[1]  # one element has trivial cost

    for i in range(2, len(s)):
        for j in range(2, k+1):
            m[i][j] = tot
            for x in range(1, i):
                cost = max(m[x][j-1], m[i][1] - m[x][1])
                if m[i][j] > cost:
                    m[i][j] = cost
                    d[i][j] = x
    part = []
    reconstruct_partition(s, d, len(s)-1, k, part)
    return part


            







