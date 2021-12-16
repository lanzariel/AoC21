import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

class Node:
    def __init__(self, name, pos):
        self.name = name
        self.neighbors = []
    
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
    
    def is_small(self):
        return ord(self.name[0 >= 97])

def binary_write(n, size):
    two_pow = 2**(size-1)
    ans = []
    for i in range(size):
        if n >= two_pow:
            ans.append(1)
            n -= two_pow
        else:
            ans.append(0)
        two_pow = two_pow//2
    return ans

def binary_read(bin):
    two_pow = 2**(len(bin)-1)
    ans = 0
    for digit in bin:
        ans += digit*two_pow
        two_pow = two_pow//2
    return ans

def was_visited(bin, index):
    return bin[index]==1

def visited_counterpart(bin, index):
    ans = bin.copy()
    ans[index] = 1
    return ans

class Graph:
    def __init__(self, edges):
        self.start = Node('start')
        self.end = Node('end')
        self.nodes = [self.start, self.end]
        self.smalls = [self.start, self.end]
        self.finder = dict()
        self.finder['start'] = self.start
        self.finder['end'] = self.end
        for e in edges:
            start, end = e.split('-')
            s_node = self.adder_of_node(start)
            e_node = self.adder_of_node(end)
            s_node.add_neighbor(e_node)
            e_node.add_neighbor(s_node)
        n_smalls = len(self.smalls)
        #self.states = [binary_write(i, n_smalls) for i in range(2**n_smalls)]
        self.n_paths = dict()
        for n in self.nodes:
            self.n_paths[n.name] = [0 for col in range(2**n_smalls)]
        self.n_paths["start"][2**(n_smalls-1)] = 1
        self.to_process = [self.start]

    def step(self):
        new_to_process = []
        for el in self.to_process:
            new_to_process.append(self.finder[''])
        self.to_process = new_to_process
    
    def solve(self):
        while len(self.to_process) > 0:
            self.to_process()
        return sum(self.n_paths[self.end])

    def adder_of_node(self, name):
        if name not in self.finder:
            new_node = Node(name)
            self.finder[name] = new_node
            self.nodes.append(new_node)
            if new_node.is_small():
                self.smalls.append(name)
            return new_node
        else:
            return self.nodes[self.finder[name]]

tra = binary_write(6,4)
print(tra)
tre = binary_read(tra)
print(tre)
print(was_visited(tra, 0))
print(visited_counterpart(tra,0))