

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
                    

def bfs(g, s, process_early=None, process_edge=None, process_late=None):
    process_early = process_early or (lambda x: x)
    process_edge = process_edge or (lambda x, y: x)
    process_late = process_late or (lambda x: x)

    discovered = [False for i in range(g.nv)]
    processed = [False for i in range(g.nv)]
    parent = [None for i in range(g.nv)]

    discovered[s] = True
    q = [s]
    while q:
        v = q.pop(0)  # fifo
        process_early(v)
        processed[v] = True

        p = g.edges[v]
        while p:
            y = p.y
            if not processed[y] or g.directed:  # accurate edge count
                process_edge(v, y)
            if not discovered[y]:
                q.append(y)
                discovered[y] = True
                parent[y] = v
            p = p.nextedge
        process_late(v)
    return parent

def findpath(g, start, end):
    parents = bfs(g, start)  # must have start as root
    if start == end or end is None:
        return start
    else:
        pass


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

