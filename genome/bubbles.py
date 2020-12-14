#python3
import sys
from itertools import combinations

class Bubbles:
    def __init__(self, k, t, reads):
        self.k = k
        self.t = t
        self.reads = reads
        self.kmers = self.make_kmers(reads, k)
        self.graph = dict()
        self.paths = dict()
        self.bubbles = 0

    def make_kmers(self, reads, k):
        kmers = set()
        n = len(reads[0])
        for read in reads:
            for i in range(n-k+1):
                kmers.add(read[i:i+k])
        return list(kmers)

    def build_graph(self):
        for kmer in self.kmers:
            pref, suff = kmer[:-1], kmer[1:]
            if pref != suff:
                self.graph.setdefault(pref, [set(), 0])
                self.graph.setdefault(suff, [set(), 0])
                if not suff in self.graph[pref][0]:
                    self.graph[pref][0].add(suff)
                    self.graph[suff][1] += 1

    def bubble(self):
        for key, val in self.graph.items():
            # print(val)
            if len(val[0]) > 1:
                self.dfs([key], key, key, 0)

        for values in self.paths.values():
            if len(values) < 2:
                continue
            for pairs in combinations(values, 2):
                if len(set(pairs[0]) & set(pairs[1])) == 2:
                    self.bubbles+=1
        
        print(self.bubbles)


    def dfs(self, path, start, current, depth):

        if (current != start) and (self.graph[current][1] > 1):
            self.paths.setdefault((start, current), list()).append([x for x in path])
        if depth == self.t:
            return

        for child in self.graph[current][0]:
            if not child in path:
                path.append(child)
                self.dfs(path, start, child, depth+1)
                path.remove(child)



k, t = map(int, input().split())
reads = list(set(sys.stdin.read().split()))
bubs = Bubbles(k,t,reads)
bubs.build_graph()
bubs.bubble()
