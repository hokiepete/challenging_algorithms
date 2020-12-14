#python3


n = int(input().strip())
# nodes = {}
N = 2**n
graph = [[] for _ in range(N)]
for i in range(N):
    # nodes[i] = str(bin(i)[2:]).zfill(n)
    graph[i].append((i*2)%N)
    graph[i].append((i*2)%N+1)
# print(graph)
# print(nodes)

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
print(''.join(map(str, [x%2 for x in circuit[::-1][:-1]])))