#python3

n, m = map(int, input().split())

graph = [[] for _ in range(n)]
rever = [[] for _ in range(n)]

for _ in range(m):
    a, b = map(int, input().split())
    graph[a-1].append(b-1)
    rever[b-1].append(a-1)

set = 1
for i in range(n):
    if len(graph[i]) != len(rever[i]):
        set = 0
        break

print(set)



if set:
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
    print(' '.join(map(str, [x+1 for x in circuit[::-1][:-1]])))
