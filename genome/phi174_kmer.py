#python3


# n = input().strip()
# nodes = {}
N = 5396
nodes = set()
edges = []
for i in range(N):
    ins = input().strip()
    lmer = ins[:-1]
    rmer = ins[1:]
    nodes.add(lmer)
    nodes.add(rmer)
    edges.append((lmer, rmer))
nodes = list(nodes)
node_map = {}
for id, node in enumerate(nodes):
    node_map[node] = id

# print(node_map)
# print(nodes)
# print(edges)

graph = [[] for _ in range(len(nodes))]
# rever = [[] for _ in range(len(nodes))]

for edge in edges:
    graph[node_map[edge[0]]].append(node_map[edge[1]])
    # rever[node_map[edge[1]]].append(node_map[edge[0]])

# print(graph)
# print(rever)
current_path = [0]
circuit = []
while current_path:
    # print(current_path)
    # print(circuit)
    current_node = current_path[-1]
    if graph[current_node]:
        current_path.append(graph[current_node].pop())
    else:
        circuit.append(current_path.pop())
print(''.join([nodes[i][0] for i in circuit[:-1][::-1]]))

# ATGC
# ATGG
# TGCC
# GCCA
# CCAT
# CATG
# GATG
# TGGG
# GGGA
# GGAT
#####
# TACT
# ACTC
# CTCC
# TCCT
# CCTC
# CTCC
# TCCA
# CCAT
# CATA
# ATAC