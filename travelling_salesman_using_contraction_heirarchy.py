#!/usr/bin/python3


import sys
import queue

# Maximum allowed edge length
maxlen = 2 * 10**6


class ContractionHeirarchy:
    def __init__(self, n, adj, cost):
        # See description of these parameters in the starter for friend_suggestion
        self.n = n
        self.INFINITY = n * maxlen
        self.adj = adj
        self.cost = cost
        # Levels of nodes for node ordering heuristics
        self.level = [0] * n
        # Positions of nodes in the node ordering
        self.rank = [0] * n
        self.contracted = [False] * n
        self.contracted_neighbors = [0] * n
        
        # Preprocess
        # initialize queue
        q = queue.PriorityQueue()
        # simulate contraction
        for v in range(self.n):
            importance, _ = self.shortcut(v, 1)
            q.put((importance, v))
        # run main
        rank = 0
        while not q.empty():
            _, v = q.get()
            importance, shortcuts = self.shortcut(v, 4)  
            if not q.empty() and importance > self.peek(q):
                q.put((importance, v))  
            else:
                self.contract(v, shortcuts)
                self.rank[v] = rank
                rank += 1
    
    @staticmethod
    def peek(pq):
        importance, node = pq.get()
        pq.put((importance, node))
        return importance
                
    # Makes shortcuts for contracting node v
    def shortcut(self, v, hops=1):
        # Implement this method yourself
        # Compute the node importance in the end
        shortcut_count = 0
        shortcut_cover = 0
        # Compute correctly the values for the above heuristics before computing the node importance
        shortcuts= []
        pred = []
        succ = []
        m_uv = 0
        m_vw = 0
        for cost, vertex in zip(self.cost[1][v], self.adj[1][v]):
            if not self.contracted[vertex]:
                pred.append((cost, vertex))
            m_uv = max(m_uv, cost)
        for cost, vertex in zip(self.cost[0][v], self.adj[0][v]):
            if not self.contracted[vertex]:
                succ.append((cost, vertex))
            m_uv = max(m_vw, cost)
        covered = set()
        m_uw = m_uv + m_vw
        for c_uv, u in pred:
            for c_vw, w in succ:
                luw = c_uv + c_vw
                m_ww = 0
                if self.cost[1][w]:
                    m_ww = max(self.cost[1][w])
                if  self.dijkstra(v,u,w, hops, m_uw - m_ww) > luw:
                    #print('add shortcut, {}'.format(luw))
                    shortcuts.append((u,w, luw))
                    shortcut_count += 1
                    if not u in covered:
                        shortcut_cover += 1
                        covered.add(u)
                    if not w in covered:
                        shortcut_cover += 1
                        covered.add(w)

        #print(shortcut_count, neighbors, shortcut_cover, self.level[v])
        importance = (shortcut_count - len(self.adj[0][v]) - len(self.adj[1][v])) + 2*self.contracted_neighbors[v] + shortcut_cover + self.level[v]
        return importance, shortcuts

    def dijkstra(self, v, u, w, max_hops, max_dist):
        #write your code here
        trip_cost = [self.INFINITY] * self.n
        trip_cost[u] = 0
        q = queue.PriorityQueue()
        q.put((trip_cost[u], u, 0))
        while not q.empty():
            _, x, hop = q.get()
            if hop > max_hops or trip_cost[x] > max_dist:
                continue
            for idx, y in enumerate(self.adj[0][x]):
                if y == v or self.contracted[y]:
                    continue
                cost = trip_cost[x] + self.cost[0][x][idx]
                if trip_cost[y] > cost:
                    trip_cost[y] = cost
                    q.put((trip_cost[y], y, hop+1))
        return trip_cost[w]

    def update_neighbors(self, v):
        for u in self.adj[0][v]:
            self.level[u] = max(self.level[u], self.level[v] + 1)
            self.contracted_neighbors[u] += 1
        for w in self.adj[1][v]:
            self.level[w] = max(self.level[w], self.level[v] + 1)
            self.contracted_neighbors[w] += 1

    def contract(self, v, shortcuts):
        self.contracted[v] = True
        self.update_neighbors(v)
        for u, w, c in shortcuts:
            self.add_arc(u, w, c)

    def add_arc(self, u, v, c):
        def update(adj, cost, u, v, c):
            for i in range(len(adj[u])):
                if adj[u][i] == v:
                    cost[u][i] = min(cost[u][i], c)
                    return
            adj[u].append(v)
            cost[u].append(c)
        update(self.adj[0], self.cost[0], u, v, c)
        update(self.adj[1], self.cost[1], v, u, c)
        
    def process(self, u, q, side):
        for idx, v in enumerate(self.adj[side][u]):
            if self.rank[u] < self.rank[v] and self.dist[side][v] > self.dist[side][u] + self.cost[side][u][idx]:
                self.dist[side][v] = self.dist[side][u] + self.cost[side][u][idx]
                q.put((self.dist[side][v], v))
        self.proc[(side + 1) % 2].add(u)

    def query(self, s, t):
        self.proc = [set(), set()]
        #print(self.rank)
        #print(self.level)
        q =[queue.PriorityQueue(), queue.PriorityQueue()]
        self.dist = [[self.INFINITY] * self.n, [self.INFINITY] * self.n]
        self.dist[0][s] = 0
        q[0].put((0,s))
        self.dist[1][t] = 0
        q[1].put((0,t))
        estimate = self.INFINITY
        while not q[0].empty() or not q[1].empty():
            if not q[0].empty():
                _, vf = q[0].get()
                if self.dist[0][vf] <= estimate:
                    self.process(vf, q[0], 0)
                if vf in self.proc[1] and self.dist[0][vf] + self.dist[1][vf] < estimate:
                    estimate = self.dist[0][vf] + self.dist[1][vf]
            if not q[1].empty():
                _, vr = q[1].get()
                if self.dist[1][vr] <= estimate:
                    self.process(vr, q[1], 1)
                if vr in self.proc[0] and self.dist[0][vr] + self.dist[1][vr] < estimate:
                    estimate = self.dist[0][vr] + self.dist[1][vr]
        return -1 if estimate == self.INFINITY else estimate



INF = 10 ** 9


# Returns the adjacency matrix of a graph on the given vertices with edges equal to the distances between
# those nodes in the initial road network
def make_graph(ch, vertices):
    n = next(vertices)
    vertices = list(vertices)
    assert n == len(vertices)
    graph = [[INF] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            l = ch.query(vertices[i]-1, vertices[j]-1)
            graph[i][j] = l if l != -1 else INF
    return graph


from itertools import combinations

def optimal_path(graph):
    a = len(graph)
    S = tuple(range(1, a))
    c = {}
    for i in range(1, a):
        c[( tuple([i]), i )] = graph[0][i]
    
    for s in range(2, a):
        for sub in combinations(S, s):
            subset = tuple(sub)
            string = subset
            for k in subset:
                sub_diff = tuple(q for q in subset if q!=k)
                str_diff = sub_diff
                for m in sub_diff:
                    if ( string, k ) in c.keys():
                        c[(string, k )] = min(c[( string, k )], c[( str_diff, m )] + graph[m][k])
                    else:
                        c[( string, k )] = c[( str_diff, m )] + graph[m][k]
    opt = INF     
    string = S
    #print(c)
    for s in S:
        #print(( str(S), s ))
        opt = min(opt, c[( string, s )] + graph[s][0])
    return -1 if opt >= INF else opt


def readl():
        return map(int, sys.stdin.readline().split())


if __name__ == '__main__':
    n,m = readl()
    adj = [[[] for _ in range(n)], [[] for _ in range(n)]]
    cost = [[[] for _ in range(n)], [[] for _ in range(n)]]
    for e in range(m):
        u,v,c = readl()
        adj[0][u-1].append(v-1)
        cost[0][u-1].append(c)
        adj[1][v-1].append(u-1)
        cost[1][v-1].append(c)

    ch = ContractionHeirarchy(n, adj, cost)
    print("Ready")
    sys.stdout.flush()
    t, = readl()
    for i in range(t):
        print(optimal_path(make_graph(ch, readl())))
