

class DoubleLink(object):
    def __init__(self, key=None, val=None, prev=None, nxt=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = nxt


class LinkedList(object):
    def __init__(self):
        self.nil = DoubleLink()
        self.nil.next = self.nil
        self.nil.prev = self.nil

    def insert(self, k, v=None):
        x = DoubleLink(k, v)
        x.next = self.nil.next
        x.prev = self.nil
        self.nil.next.prev = x
        self.nil.next = x

    def listsearch(self, k):
        x = self.nil.next
        while x is not self.nil and x.key != k:
            x = x.next
        if x.key:
            return x

    def delete(self, k):
        x = self.listsearch(k)
        if x:
            x.prev.next = x.next
            x.next.prev = x.prev
        return x



