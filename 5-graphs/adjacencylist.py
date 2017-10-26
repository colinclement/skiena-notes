

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
    
    def findpath(self, start, end):
        parents = self.bfs(start)  # must have start as root
        if start == end or end is None:
            return [start]
        else:
            endp = parents[end]
            path = [endp, end]
            while not endp == start:
                endp = parents[endp]
                path = [endp] + path
            return path

    def connected_components(self):
        components = []
        def addcomponents(x, comp):
            comp += [x]
    
        comp = []
        self.process_early = lambda x: addcomponents(x, comp)
        self.bfs(0)  # start search from arbitrary node
        components += [comp]

        for i in range(self.nv):
            if not self._discovered[i]:
                comp = []
                self.process_early = lambda x: addcomponents(x, comp)
                self.bfs(i)
                components += [comp]
        return components


if __name__=="__main__":
    g = Graph(7)  # one extra so we can pretend to index from 1
    g.insert(1, 2)
    g.insert(1, 5)
    g.insert(1, 6)
    g.insert(2, 5)
    g.insert(2, 3)
    g.insert(3, 4)
    g.insert(4, 5)
    g.show()

