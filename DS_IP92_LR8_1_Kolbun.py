# s - power of incoming = 0
# t - power of outcoming = 0
from collections import defaultdict

class Graph:
    def __init__(self, v_num, e_num):
        self.v_num = v_num
        self.e_num = e_num
        self.adj_list = defaultdict(list)
        self.flow = defaultdict(list)
        self.graph = []

    def __str__(self):
        return "\n".join(["".join(map(lambda x: x.ljust(4), map(str, row))) for row in self.flow_matrix()])

    def flow_matrix(self):
        matrix = [[0] * self.v_num for _ in range(self.v_num)]
        for u, v, w in self.graph:
            matrix[u][v] = w
        return matrix

    def get_min_row(self, matr):
        arr = []
        for row in matr:
            if sum(row) == 0:
                v = matr.index(row)
        return v

    def find_s_t(self):
        source = self.get_min_row(list(map(list, zip(*self.flow_matrix()))))  # source
        target = self.get_min_row(self.flow_matrix())
        return source, target

    def add_edge(self, u, v, w=0):
        edge = [u-1, v-1, w]
        res_edge = [u-1, v-1, 0]
        if u == v:
            raise ValueError("u == v")
        self.graph.append(edge)
        self.adj_list[u].append(v)
        edge, res_edge = res_edge, edge
        # Intialize all flows to zero
        self.flow[u-1] = 0
        self.flow[res_edge] = 0



class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}

    def AddVertex(self, vertex):
        self.adj[vertex] = []

    def GetEdges(self, v):
        return self.adj[v]

    def AddEdge(self, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u, v, w)
        redge = Edge(v, u, 0)
        edge.redge = redge
        redge.edge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        # Intialize all flows to zero
        self.flow[edge] = 0
        self.flow[redge] = 0

    def FindPath(self, source, target, path):
        if source == target:
            return path
        for edge in self.GetEdges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and not (edge, residual) in path:
                result = self.FindPath(edge.target, target, path + [(edge, residual)])
                if result != None:
                    return result

    def MaxFlow(self, source, target):
        path = self.FindPath(source, target, [])
        print('path after enter MaxFlow: %s' % path)
        for key in self.flow:
            print('%s:%s' % (key, self.flow[key]))
        print('-' * 20)
        while path is not None:
            flow = min(res for edge, res in path)
            for edge, res in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            for key in self.flow:
                print('%s:%s' % (key, self.flow[key]))
            path = self.FindPath(source, target, [])
            print('path: %s' % path)
        for key in self.flow:
            print('%s:%s' % (key, self.flow[key]))
        return sum(self.flow[edge] for edge in self.GetEdges(source))


input_file = open('graph.txt')
v_num, e_num = map(int, input_file.readline().split())
graph = Graph(v_num, e_num)
for line in input_file:
    graph.add_edge(*map(int, line.split()))
input_file.close()

print(graph)
print(graph.find_s_t())
graph.FlowNetwork()