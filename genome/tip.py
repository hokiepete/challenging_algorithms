#python3
import sys
from itertools import combinations

class Bubbles:
    def __init__(self, k, reads):
        self.k = k
        self.reads = reads
        self.kmers = self.make_kmers(reads, k)
        self.graph = dict()
        self.rever = dict()
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
                self.graph.setdefault(pref, set())
                self.graph.setdefault(suff, set())
                self.rever.setdefault(pref, set())
                self.rever.setdefault(suff, set())
                if not suff in self.graph[pref]:
                    self.graph[pref].add(suff)
                    self.rever[suff].add(pref)
                    
    def bubble(self, t):
        for key, val in self.graph.items():
            # print(val)
            if len(val) > 1:
                self.dfs([key], key, key, 0, t)

        for values in self.paths.values():
            if len(values) < 2:
                continue
            for pairs in combinations(values, 2):
                if len(set(pairs[0]) & set(pairs[1])) == 2:
                    self.bubbles+=1
        
        print(self.bubbles)

    def dfs(self, path, start, current, depth, t):

        if (current != start) and (len(self.rever[current]) > 1):
            self.paths.setdefault((start, current), list()).append([x for x in path])
        if depth == t:
            return

        for child in self.graph[current]:
            if not child in path:
                path.append(child)
                self.dfs(path, start, child, depth+1, t)
                path.remove(child)

    def tips(self):
        tip = 0
        run  = True
        while run:
            for key, val in list(self.graph.items()):
                # print(key, val)
                if len(val) == 0:
                    tip += 1
                    # print('yes')
                    for elem in list(self.rever[key]):
                        self.graph[elem].remove(key)
                        self.rever[key].remove(elem)
                        
                    del self.graph[key], self.rever[key]
                    break
            else:
                run = False

        run  = True
        while run:
            for key, val in list(self.rever.items()):
                # print(key, val)
                if len(val) == 0:
                    tip += 1
                    # print('yes')
                    for elem in list(self.graph[key]):
                        self.rever[elem].remove(key)
                        self.graph[key].remove(elem)

                    del self.graph[key], self.rever[key]
                    break
            else:
                run = False

        # print(self.graph)
        # print(self.rever)
        print(tip)



#k, t = map(int, input().split())
k = 15
reads = list(set(sys.stdin.read().split()))
bubs = Bubbles(k,reads)
bubs.build_graph()
#bubs.bubble(t)

bubs.tips()