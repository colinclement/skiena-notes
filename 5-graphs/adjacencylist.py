

class Edgenode(object):
    def __init__(self, y=None, w=1):
        self.y = None 
        self.w = 1
        self.nextedge = None

class Graph(object):
    def __init__(self, nvertices, nedges, directed=True):
        self.nv = nvertices
        self.ne = nedges

        self.degress = [0 for i in range(self.nv)]
        self.edges = []

