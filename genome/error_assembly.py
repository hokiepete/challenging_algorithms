# python3
import sys
from collections import deque

sys.setrecursionlimit(200000)


class Kmers:

    def __init__(self):
        self.id = 0
        self.ids_map = dict()
        self.kmers = dict()

    def insert(self, kmer):
        if kmer not in self.ids_map:
            self.ids_map[kmer] = self.id
            self.kmers[self.id] = kmer
            self.id += 1
        return self.ids_map[kmer]


class Assembler:

    def __init__(self, k, reads):
        self.k = k
        self.reads = reads
        self.thresh = k + 1
        self.kmer_ids = Kmers()
        self.paths = dict()
        self.coverage = dict()
        self.graph = dict()

    def outgoing_num(self, x):
        return len(self.graph[x][0])

    def incoming_num(self, x):
        return self.graph[x][1]

    def make_kmers(self):
        def break_read(read):
            return [
                read[i:i+self.k] for i in range(
                    len(read) - self.k + 1
                )
            ]
        self.kmers = [
            kmer for read in self.reads for kmer in break_read(read)
        ]

    def build_graph(self):
        def add_edge(pref, suff):
            self.graph.setdefault(pref, [set(), 0])
            self.graph.setdefault(suff, [set(), 0])
            self.coverage.setdefault((pref, suff), 0)
            self.coverage[(pref, suff)] += 1

            if suff not in self.graph[pref][0]:
                self.graph[pref][0].add(suff)
                self.graph[suff][1] += 1

        self.make_kmers()
        for kmer in self.kmers:
            pref = self.kmer_ids.insert(kmer[:-1])
            suff = self.kmer_ids.insert(kmer[1:])

            if pref != suff:
                add_edge(pref, suff)

    def remove_leaves(self):
        for key, val in list(self.graph.items()):
            if len(val[0]) == 0:
                del self.graph[key]

    def remove_tips(self):
        for key, val in self.graph.items():
            if (self.outgoing_num(key) == 1) and (self.incoming_num(key) == 0):
                find_and_remove = self.find_and_remove_in
            elif (self.outgoing_num(key) > 1):
                find_and_remove = self.find_and_remove_out
            else:
                continue

            run = True
            while run:
                run = False
                for child in val[0]:
                    if find_and_remove(child, 0):
                        val[0].remove(child)
                        run = True
                        break

    def find_and_remove_out(self, current, depth):
        if (self.outgoing_num(current) > 1) \
                or (self.incoming_num(current) > 1):
            return False

        if depth == self.thresh:
            return False

        if self.outgoing_num(current) == 0:
            return True

        child = next(iter(self.graph[current][0]))
        if self.find_and_remove_out(child, depth + 1):
            self.graph[current][0].pop()
            self.graph[child][1] -= 1
            return True
        return False

    def find_and_remove_in(self, current, depth):
        if (self.outgoing_num(current) == 0) \
                or (self.incoming_num(current) > 1):
            return True

        if depth == self.thresh:
            return False

        child = next(iter(self.graph[current][0]))
        if self.find_and_remove_in(child, depth + 1):
            self.graph[current][0].pop()
            self.graph[child][1] -= 1
            return True
        return False

    def remove_bubbles(self):
        for key in self.graph.keys():
            if self.outgoing_num(key) > 1:
                self.dfs(path=[key], current=key, depth=0)

        for pair, candidates in self.paths.items():
            src, tgt = pair
            best = max(candidates, key=lambda x: x[1])[0]
            for path, _ in candidates:
                if (best == path) or not self.bubble_possible(src, tgt):
                    continue
                if self.paths_disjoint(best, path) and self.path_exists(path):
                    self.remove_path(path)

    def bubble_possible(self, src, tgt):
        return (len(self.graph[src][0]) > 1) and (self.graph[tgt][1] > 1)

    def path_exists(self, path):
        for i in range(len(path) - 1):
            if path[i+1] not in self.graph[path[i]][0]:
                return False
        return True

    def remove_path(self, path):
        for i in range(len(path) - 1):
            self.graph[path[i]][0].remove(path[i+1])
            self.graph[path[i+1]][1] -= 1
            del self.coverage[(path[i], path[i+1])]

    @staticmethod
    def paths_disjoint(path1, path2):
        return len(set(path1) & set(path2)) == 2

    def dfs(self, path, current, depth):
        if (current != path[0]) and (self.incoming_num(current) > 1):
            weight = (1/len(path)) * sum(
                self.coverage[(path[i], path[i+1])] for i in range(len(path) - 1)
            )
            self.paths.setdefault((path[0], current), list()).append(([x for x in path], weight))

        if depth == self.thresh:
            return

        for child in self.graph[current][0]:
            if child not in path:
                path.append(child)
                self.dfs(path, child, depth+1)
                path.remove(child)

    def cycle(self):
        queue = deque()
        circuit = []
        current = next(iter(self.graph))
        queue.append(current)

        while queue:
            current = queue[0]
            if len(self.graph[current][0]) != 0:
                child = next(iter(self.graph[current][0]))
                queue.append(child)
                self.graph[current][0].remove(child)
                continue
            circuit.append(current)
            queue.popleft()

        return circuit


k = 20
reads = sys.stdin.read().split()
genome = Assembler(k, reads)
genome.build_graph()
genome.remove_tips()
genome.remove_leaves()
genome.remove_bubbles()
cycle = genome.cycle()
ids = genome.kmer_ids
circle = ids.kmers[cycle[0]]
for i in range(1, len(cycle) - (k - 1)):
    circle += ids.kmers[cycle[i]][-1]

print(circle)
