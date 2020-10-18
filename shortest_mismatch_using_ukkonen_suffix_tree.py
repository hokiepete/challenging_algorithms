# python3
import sys
import queue
from operator import attrgetter
sys.setrecursionlimit(200000)

LEAF_END = -1

class Node:
    def __init__(self, leaf):
        self.children = {}
        self.leaf = leaf
        self.suffix_index = None
        self.start = None
        self.end = None
        self.suffix_link = None
        self.all_l_children = False
        
    def __eq__(self, node):
        atg = attrgetter('start', 'end', 'suffix_index')
        return atg(self) == atg(node)
    
    def __ne__(self, node):
        atg = attrgetter('start', 'end', 'suffix_index')
        return atg(self) != atg(node)
    
    def __getattribute__(self, name):
        if name == 'end' and self.leaf:
            return LEAF_END
        return super(Node, self).__getattribute__(name)
    
    def __str__(self):
        return str(self.children.items())
    
class SuffixTree:
    
    def __init__(self, data):
        self.text = data
        self.last_new_node = None
        self.active_node = None
        self.active_edge = -1
        self.active_len = 0
        self.remaining_suffix_cnt = 0
        self.root_end = None
        self.split_end = None
        self.size = -1
        self.root = None
        
    def edge_length(self, node):
        return node.end - node.start + 1
    
    def walk_down(self, current_node):
        length = self.edge_length(current_node)
        if self.active_len >= length:
            self.active_edge += length
            self.active_len -= length
            self.active_node = current_node
            return True
        return False
    
    def make_node(self, start, end=None, leaf=False):
        node = Node(leaf)
        node.suffix_link = self.root
        node.start = start
        node.end = end
        node.suffix_index = -1
        return node

    def extend(self, pos):
        global LEAF_END
        LEAF_END = pos
        self.remaining_suffix_cnt += 1
        self.last_new_node = None
        
        while self.remaining_suffix_cnt > 0:
            
            if self.active_len == 0:
                self.active_edge = pos
            if self.active_node.children.get(self.text[self.active_edge]) is None:
                # print('if')
                self.active_node.children[
                    self.text[self.active_edge]
                    ] = self.make_node(pos, leaf=True)
                
                if self.last_new_node is not None:
                    self.last_new_node.suffix_link = self.active_node
                    self.last_new_node = None
            
            else:
                # print('else')
                _next = self.active_node.children.get(
                    self.text[self.active_edge])
                
                if self.walk_down(_next):
                    continue
                
                if self.text[
                        _next.start + self.active_len] == self.text[pos]:
                    
                    if (self.last_new_node is not None) and (
                            self.active_node != self.root):
                        self.last_new_node.suffix_link = self.active_node
                        self.last_new_node = None
                    
                    self.active_len += 1
                    break
            
                self.split_end = _next.start + self.active_len - 1
                
                split = self.make_node(_next.start, self.split_end)
                self.active_node.children[self.text[self.active_edge]] = split
                
                split.children[self.text[pos]] = self.make_node(pos, leaf=True)
                _next.start += self.active_len
                split.children[self.text[_next.start]] = _next
                
                if self.last_new_node is not None:
                    self.last_new_node.suffix_link = split
                
                self.last_new_node = split
            # print('end if')
            self.remaining_suffix_cnt -= 1
            
            if (self.active_node == self.root) and (self.active_len > 0):
                # print('this')
                self.active_len -= 1
                self.active_edge = pos - self.remaining_suffix_cnt + 1
            
            elif self.active_node != self.root:
                # print('that')
                self.active_node = self.active_node.suffix_link
                
    def build_tree(self):
        self.size = len(self.text)
        
        self.root_end = -1
        self.root = self.make_node(-1, self.root_end)
        self.active_node = self.root
        for i in range(self.size):
            self.extend(i)
        
    def walk_dfs(self, current):
        start, end = current.start, current.end
        yield self.text[start:end+1]
        
        for node in current.children.values():
            if node:
                yield from self.walk_dfs(node)

class SuffixSearch:
    def __init__(self, tree, lp, lq, p, q):
        self.tree = tree
        self.lp = lp
        self.lq = lq
        self.p = p
        self.q = q
        self.candidates = []

    def is_l_leaf(self, node):
        return node.leaf and node.start <= self.lp
    
    def bfs(self):
        pq = queue.Queue()
        pq.put(('', self.tree.root))
        while not pq.empty():
            path, node = pq.get()
            if self.is_l_leaf(node) and node.start == self.lp and path:
                #print(f'is empty l leaf, {path}')
                if not path in self.q:
                    self.candidates.append([len(path), path])
                continue
            elif self.is_l_leaf(node) and node.start != self.lp:
                new_path = path + self.tree.text[node.start]
                #print(f'is l leaf, {new_path}')
                if not new_path in self.q:
                    self.candidates.append([len(new_path), new_path])
                continue
            elif node.all_l_children:
                new_path = path + self.tree.text[node.start: node.end+1]
                #print(f'all children are l leaf, {new_path}')
                if not new_path in self.q:
                    self.candidates.append([len(new_path), new_path])
                continue
            new_path = path + self.tree.text[node.start:node.end+1]
            for child in node.children.values():
                pq.put((new_path, child))
            
    def recurse(self, node):
        if node.leaf:
            return node.start <= self.lp
        child_stat = []
        for child in node.children.values():
            child_stat.append(self.recurse(child))
        if child_stat and all(child_stat):
            node.all_l_children = True  
            return True          
        return False

def solve (p, q):
    lp = len(p)
    lq = len(q)
    st = SuffixTree(p+'#'+q+'$')
    st.build_tree()
    ss = SuffixSearch(st, lp, lq, p, q)
    #print(list(st.walk_dfs(st.root)))
    ss.recurse(ss.tree.root)
    ss.bfs()
    ss.candidates.sort()
    #print(ss.candidates)
    return min(ss.candidates)[1]
    # for _, cand in ss.candidates:
    #     if not cand in q:
    #         return cand
        
    # for res in st.walk_dfs(st.root):
    #     if res:
    #         print(res)
    
    # result = ''
    
    # return result

p = sys.stdin.readline ().strip ()
q = sys.stdin.readline ().strip ()

ans = solve (p, q)

sys.stdout.write (ans + '\n')
