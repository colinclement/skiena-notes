import ll

class HashTable(object):
    def __init__(self, m=8, hashfunc=None):
        self.m = m
        self.t = [ll.LinkedList() for i in range(m)]
        self.n = 0
        self.hashfunc = hashfunc
        if hashfunc is None:
            self.hashfunc = lambda x: hash(x) % self.m

    def insert(self, k, v):
        i = self.hashfunc(k)
        x = self.t[i].listsearch(k)
        if x:  # if this key already exists, over-write
            x.v = v
        else:
            self.t[i].insert(k, v)
            self.n += 1

    def search(self, k):
        i = self.hashfunc(k)
        return self.t[i].listsearch(k).val

    def delete(self, k):
        i = self.hashfunc(k)
        if self.t[i].delete(k):
            self.n -= 1
