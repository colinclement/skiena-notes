"""
heapsort.py

author: Colin Clement
date: 2017-10-22

This follows Skiena section 4.3, implementing the heap sort

"""

def selectionsort(l):
    lsort = []
    n = len(l)
    for i in range(n):
        lmin = min(l)
        lsort += [lmin]
        l.remove(lmin)
    return lsort


class PriorityQueue(object):
    def __init__(self, items):
        self.q = [None for i in range(len(items)+1)]  # not using first el
        self.n = 0
        [self.insert(x) for x in items]

    def parent(self, n):
        if n == 0:
            return None
        else:
            return n//2

    def youngchild(self, n):
        return 2 * n

    def insert(self, x):
        assert self.n < len(self.q), "Warning: priority queue overflow"
        self.n += 1
        self.q[self.n] = x
        self.bubbleup(self.n)

    def bubbleup(self, p):
        if not self.parent(p):
            return None
        elif self.q[self.parent(p)] > self.q[p]:
            tmp = self.q[self.parent(p)]
            self.q[self.parent(p)] = self.q[p]
            self.q[p] = tmp
            self.bubbleup(self.parent(p))

    def bubbledown(self, p):
        c = self.youngchild(p)
        minind = p
        if c <= self.n:
            if self.q[minind] > self.q[c]:  # check if children dominate
                minind = c
        if c + 1 <= self.n:
            if self.q[minind] > self.q[c + 1]:
                minind = c + 1
        if minind != p:
            tmp = self.q[p]
            self.q[p] = self.q[minind]
            self.q[minind] = tmp
            self.bubbledown(minind)

    def extractmin(self):
        mn = None
        assert self.n > 0, "Warning: empty priority queue"
        mn = self.q[1]  # min value is easy! Now to keep it that way

        self.q[1] = self.q[self.n]  # start inverting heap
        self.q[self.n] = None  # so its easier to see it working
        self.n -= 1
        self.bubbledown(1)
        return mn


class PriorityQueueFastHeap(PriorityQueue):
    """
    This can construct the heap in linear time. This is still
    dominated by the nlogn search for the minimization, as is seen
    in the complexity analysis below. We are only 100x slow than
    the system sort. This is probably because sorted is implemented in C.
    """
    def __init__(self, items):
        self.q = [None] + items
        self.n = len(items) 

        for i in range(self.n, 0, -1):
            self.bubbledown(i)

def heapsort(li):
    pq = PriorityQueue(li)
    return [pq.extractmin() for i in range(len(li))]

def heapsort_fast(li):
    pq = PriorityQueueFastHeap(li)
    return [pq.extractmin() for i in range(len(li))]

if __name__=="__main__":
    li = [1942, 1783, 1776, 1804, 1865, 1945, 1963, 1918, 2001, 1941]
    pq = PriorityQueue(li)

    import random
    import matplotlib.pyplot as plt
    from datetime import datetime

    sizes = [2**i for i in range(1, 18)]
    heaptime = []
    fastheaptime = []
    stdtime = []
    for s in sizes:
        lst = [random.randint(1,100000) for i in range(s)]
        s = datetime.now()
        lstsrt = heapsort(lst)
        heaptime += [(datetime.now() - s).total_seconds()]

        s = datetime.now()
        lstsrt = heapsort_fast(lst)
        fastheaptime += [(datetime.now() - s).total_seconds()]

        s = datetime.now()
        lstsrt = sorted(lst)
        stdtime += [(datetime.now() - s).total_seconds()]

    plt.loglog(sizes, heaptime, label='heapsort')
    plt.loglog(sizes, fastheaptime, label='heapsort')
    plt.loglog(sizes, stdtime, label='stdsort')
    plt.legend()
    plt.show()



