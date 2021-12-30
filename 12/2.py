import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

def ternary_write(n, size):
    three_pow = 3**(size-1)
    ans = []
    for i in range(size):
        digit = n//three_pow
        ans.append(digit)
        n = n-three_pow*digit
        three_pow = three_pow//3
    return ans

def ternary_read(ter):
    three_pow = 3**(len(ter)-1)
    ans = 0
    for digit in ter:
        ans += digit*three_pow
        three_pow = three_pow//3
    return ans

def was_visited(bin, index):
    return bin[index]>=2

def visited_counterpart(bin, index):
    ans = bin.copy()
    ans[index] += 1
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
        if self.name=="start":
            ans[0]=1
            return ans
        non_end_neighbors = [i for i in self.neighbors if i.name!="end"]
        for n in non_end_neighbors:
            for i in range(len(self.paths)):
                ans[i] += n.paths[i]
        if self.name=="end":
            return ans
        if self.is_small():
            real_ans = [0 for i in self.paths]
            for i in range(len(self.paths)):
                ternary_rep  = ternary_write(i, self.n_smalls)
                if not was_visited(ternary_rep, self.small_n):
                    ternary_next = visited_counterpart(ternary_rep, self.small_n)
                    next = ternary_read(ternary_next)
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
        self.smalls = []
        self.finder = dict()
        self.start.set_small_n(3000)
        self.end.set_small_n(3001)
        self.finder['start'] = self.start
        self.finder['end'] = self.end
        for e in edges:
            start, end = e.split('-')
            s_node = self.adder_of_node(start)
            e_node = self.adder_of_node(end)
            s_node.add_neighbor(e_node)
            e_node.add_neighbor(s_node)
        n_smalls = len(self.smalls)
        for n in self.nodes:
            n.set_paths([0 for col in range(3**n_smalls)])
            n.set_n_smalls(n_smalls)
        starting_path = [0 for col in range(3**n_smalls)]
        starting_path[0] = 1
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
        ans = 0
        for i in range(len(self.end.paths)):
            ternary = ternary_write(i,len(self.smalls))
            number_of_twos = 0
            for el in ternary:
                if el==2:
                    number_of_twos += 1
                    if number_of_twos > 1:
                        break
            if number_of_twos <= 1:
                ans += self.end.paths[i]
        return ans

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