
class Node(object):
    def __init__(self, k=None, l=None, r=None, p=None):
        self.k = k
        self.l = l
        self.r = r
        self.p = p

class BinaryTree(object):
    def __init__(self):
        self.head = Node()

    def insert(self, k):
        z = Node(k)
        x = self.head
        while x:
            y = x  # preorder
            if k < x.k:
                x = x.l
            else:
                x = x.r
        z.p = y
        if k < y.k:
            y.l = z
        else:
            y.r = z  # if y.k is None this always evaluated

    def search(self, k, x):
        if (x is not None) or x.k == k:
            return x
        if k < x.k:
            return self.search(k, x.l)
        else:
            return self.search(k, x.r)

    def itersearch(self, k):
        x = self.head.r
        while (x is not None) and x.k != k:
            if k < x.k:
                x = x.l
            else:
                x = x.r
        return x

    def _transplant(self, u, v):
        if u.p is self.head:
            self.head.r = v
        elif u is u.p.l:
            u.p.l = v
        elif u is u.p.r:
            u.p.r = v
        if v:
            v.p = u.p

    def delete(self, x):
        if not x.l:
            self._transplant(x, x.r)
        elif not x.r:
            self._transplant(x, x.l)
        else:  # two children
            y = self.min(x.r)
            if y.p is not x:  # successor is inside subtree
                self._transplant(y, y.r)
                y.r = x.r
                y.r.p = y
            self._transplant(x, y)
            y.l = x.l
            y.l.p = y
        

    def pred(self, x):
        if x.l:
            return self.max(x.l)
        y = x.p
        while y and x is y.l:
            x = y
            y = y.p
        return y

    def succ(self, x):
        if x.r:
            return self.min(x.r)
        y = x.p
        while y and x is y.r:  # successor is larger
            x = y
            y = y.p
        return y
    
    def min(self, x=None):
        x = x or self.head.l
        while x.l:
            x = x.l
        return x

    def max(self, x=None):
        x = x or self.head.l
        while x.l:
            x = x.r
        return x

    def inorderwalk(self, x):
        if x:
            self.inorderwalk(x.l)
            print(x.k)
            self.inorderwalk(x.r)

if __name__=="__main__":
    one = [6, 5, 7, 2, 5, 8]
    two = [2, 5, 7, 6, 8, 5]
    three = [15, 6, 18, 3, 7, 17, 20, 2, 4, 13, 9]

    bal = BinaryTree()
    [bal.insert(k) for k in one]
    unbal = BinaryTree()
    [unbal.insert(k) for k in two]
    bigger = BinaryTree()
    [bigger.insert(k) for k in three]
