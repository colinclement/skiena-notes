"""
adjacancy.py

author: Colin Clement
date: 2017-10-26

Implementation of adjacancy-list graph structure and basic graph traversal
algorithms as described in Skiena chapter 5
"""


class Edgenode(object):
    def __init__(self, y=None, w=1):
        self.y = None 
        self.w = 1
        self.nextedge = None



class Graph(object):
    def __init__(self, nvertices, directed=False):
        self.nv = nvertices
        self.ne = 0
        self.directed = directed

        self.degrees = [0 for i in range(self.nv)]
        self.edges = [None for i in range(self.nv)]

        self.process_early = lambda x: x
        self.process_edge = lambda x, y: x
        self.process_late = lambda x: x

    def insert(self, x, y, directed=False):
        p = Edgenode(y)
        p.y = y
        p.nextedge = self.edges[x]
        self.edges[x] = p
        self.degrees[x] += 1
        if not directed:
            self.insert(y, x, True)
        else:
            self.ne += 1

    def show(self):
        for i in range(self.nv):
            if self.degrees[i]:
                p = self.edges[i]
                edgestr = "vertex {}: ".format(i)
                while p:
                    edgestr += "{} ".format(p.y)
                    p = p.nextedge
                print(edgestr)
                    
    def bfs(self, s):
        self._discovered = [False for i in range(self.nv)]
        self._processed = [False for i in range(self.nv)]
        parent = [None for i in range(self.nv)]
    
        self._discovered[s] = True
        q = [s]
        while q:
            v = q.pop(0)  # fifo
            self.process_early(v)
            self._processed[v] = True
    
            p = self.edges[v]
            while p:
                y = p.y
                if not self._processed[y] or self.directed:  # accurate edge count
                    self.process_edge(v, y)
                if not self._discovered[y]:
                    q.append(y)
                    self._discovered[y] = True
                    parent[y] = v
                p = p.nextedge
            self.process_late(v)
        return parent

    def findpath(self, start, end, parents, path=None):
        path = path if path is not None else [end]
        if start == end:
            return path
        elif end is None:
            return []  # no path exists!
        else:
            return self.findpath(start, parents[end], parents, 
                                 [parents[end]] + path)
    
    def shortestpath(self, start, end):
        parents = self.bfs(start)  # must have start as root
        return self.findpath(start, end, parents)
        
    def connected_components(self):
        components = []
        def addcomponents(x, comp):
            comp += [x]
    
        comp = []
        self.process_early = lambda x: addcomponents(x, comp)
        self.bfs(0)  # start search from arbitrary node
        components += [comp]

        for i in range(1, self.nv):  # already did 0
            if not self._discovered[i]:
                comp = []
                self.process_early = lambda x: addcomponents(x, comp)
                self.bfs(i)
                components += [comp]

        self.process_early = lambda x: x  # reset process_early
        return components

    def dfs(self, s):
        self._discovered = [False for i in range(self.nv)]
        self._processed = [False for i in range(self.nv)]
        self._parent = [None for i in range(self.nv)]
        self._entry = [None for i in range(self.nv)]
        self._exit = [None for i in range(self.nv)]
        self._finished = False
        self._time = 0
        
        def search(v):
            if self._finished:
                return
            self._discovered[v] = True
            self._time += 1
            self._entry[v] = self._time
            self.process_early(v)
            p = self.edges[v]
            while p:
                y = p.y
                if not self._discovered[y]:
                    self._parent[y] = v
                    self.process_edge(v, y)

                    search(y)

                elif not self._processed[y] or self.directed:
                    self.process_edge(v, y)
                    if self._finished:
                        return
                p = p.nextedge

            self.process_late(v)
            self._time += 1
            self._exit[v] = self._time
            self._processed[v] = True

        search(s)
        return self._parent, self._entry, self._exit

    def findcycle(self, x, y):
        # STILL BROKE!
        cycle = []
        def process_edge(x, y, path=cycle):
            """ Note the subtle conditionals for finding a back edge. """
            print("Edge ({}, {})".format(x, y))
            if self._parent[x] != y:  # Condition for a back edge!
                print("{} is not the parent of {}".format(y, x))
                print(self._parent)
                path = self.findpath(y, x, self._parent, path)
                print('path = {}'.format(path))
                self._finished = True  # stop looking!

        self.process_edge = process_edge
        self.dfs(x)
        self.process_edge = lambda x, y: x
        return cycle


if __name__=="__main__":
    g = Graph(7)  # one extra so we can pretend to index from 1
    g.insert(1, 6)
    g.insert(1, 5)
    g.insert(1, 2)
    g.insert(2, 5)
    g.insert(2, 3)
    g.insert(3, 4)
    g.insert(4, 5)
    g.show()

