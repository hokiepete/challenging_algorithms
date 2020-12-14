# python3
import queue

class Edge:

    def __init__(self, u, v, capacity, tag, lower):
        self.u = u
        self.v = v
        self.lower = lower
        self.capacity = capacity
        self.flow = 0
        self.tag = tag

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]
        self.n = n

    def reset_pred(self):
        self.pred = [None] * (self.n + 2)

    def add_edge(self, from_, to, capacity, prefix= '', lower=0):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity, prefix + 'forwards', lower)
        backward_edge = Edge(to, from_, 0, prefix + 'backwards', lower)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    inn = [0] * vertex_count
    out = [0] * vertex_count
    for _ in range(edge_count):
        u, v, demand, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity - demand, lower=demand)
        out[u-1] += demand
        inn[v-1] += demand

    graph.graph.append([])
    graph.graph.append([])
    for i in range(vertex_count):
        graph.add_edge(vertex_count, i, inn[i], prefix='aux')
        graph.add_edge(i, vertex_count + 1, out[i], prefix='aux')

    graph.lower_sum = sum(out)
    return graph


def max_flow(graph, from_, to):
    flow = 0
    # your code goes here
    run = True
    while run:
        graph.reset_pred()
        q = queue.Queue()
        q.put(from_)
        while not q.empty():
            node_id = q.get()
            for edge_id in graph.get_ids(node_id):
                edge = graph.get_edge(edge_id)
                if (graph.pred[edge.v] is None) and (edge.v != from_) and (edge.flow < edge.capacity):
                    graph.pred[edge.v] = edge_id
                    q.put(edge.v)
        
        if graph.pred[to] is None:
            run = False
        else:
            df = float('inf')
            edge_id = graph.pred[-1]
            while not edge_id is None:
                edge = graph.get_edge(edge_id)
                df = min(df, edge.capacity - edge.flow)
                edge_id = graph.pred[edge.u]
            edge_id = graph.pred[-1]
            while not edge_id is None:
                edge = graph.get_edge(edge_id)
                graph.add_flow(edge_id, df)
                edge_id = graph.pred[edge.u]
            flow += df  
    
    return flow


if __name__ == '__main__':
    graph = read_data()
    flow = max_flow(graph, graph.size() - 2, graph.size() - 1)
    if flow >= graph.lower_sum:
        print('YES')
        for edge in graph.edges:
            if edge.tag == 'forwards':
                print(edge.flow + edge.lower)
    else:
        print('NO')
