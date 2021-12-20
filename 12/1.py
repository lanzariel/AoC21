import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

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

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
    
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
    
    def is_small(self):
        return ord(self.name[0]) >= 97
    
    def set_small_n(self, n):
        self.small_n = n

    def set_paths(self, p):
        self.paths = p
    
    def set_n_smalls(self, n):
        self.n_smalls = n
    
    def neighbor_implied_paths(self):
        ans = [0 for i in self.paths]
        for n in self.neighbors:
            for i in range(len(self.paths)):
                ans[i] += n.paths[i]
        if self.is_small():
            real_ans = [0 for i in self.paths]
            for i in range(len(self.paths)):
                binary_rep  = binary_write(i, self.n_smalls)
                if not was_visited(binary_rep, self.small_n):
                    binary_next = visited_counterpart(binary_rep, self.small_n)
                    next = binary_read(binary_next)
                    real_ans[next] = ans[i]
            ans = real_ans
        return ans
    
    def was_updated(self):
        was_updated = False
        new_paths = self.neighbor_implied_paths()
        for i in range(len(self.paths)):
            if self.paths[i] != new_paths[i]:
                self.paths[i] = new_paths[i]
                was_updated = True
        return was_updated

class Graph:
    def __init__(self, edges):
        self.start = Node('start')
        self.end = Node('end')
        self.nodes = [self.start, self.end]
        self.smalls = [self.start, self.end]
        self.finder = dict()
        self.start.set_small_n(0)
        self.end.set_small_n(1)
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
        #self.n_paths = dict()
        for n in self.nodes:
            n.set_paths([0 for col in range(2**n_smalls)])
            n.set_n_smalls(n_smalls)
        starting_path = [0 for col in range(2**n_smalls)]
        starting_path[2**(n_smalls-1)] = 1
        self.start.set_paths(starting_path)
        self.to_process = [self.start]

    def step(self):
        new_to_process = set()
        for el in self.to_process:
            for n in el.neighbors:
                if n.was_updated():
                    new_to_process.add(n)
        self.to_process = list(new_to_process)
    
    def solve(self):
        while len(self.to_process) > 0:
            self.step()
        return sum(self.finder['end'].paths)

    def adder_of_node(self, name):
        if name not in self.finder:
            new_node = Node(name)
            self.finder[name] = new_node
            self.nodes.append(new_node)
            if new_node.is_small():
                new_node.set_small_n(len(self.smalls))
                self.smalls.append(new_node)
            return new_node
        else:
            return self.finder[name]

g = Graph(lines)
print(g.solve())