import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

class Number:
    def __init__(self, string, father):
        self.father = father
        if father == -1:
            self.level = 0
            self.root = self
            self.leaves = []
        else:
            self.level = self.father.level + 1
            self.root = self.father.root
        if string[0] == "[":
            self.is_number = False
            self.s1 = Number(string[1:], self)
            other_string = self.s1.rest
            self.s2 = Number(other_string[1:], self)
            self.rest = self.s2.rest[1:]
            self.update_magnitude()
        else:
            self.is_number = True
            self.magnitude = int(string[0])
            self.rest = string[1:]
            self.index_n = len(self.root.leaves)
            self.root.leaves.append(self)
    
    def update_magnitude(self):
        self.magnitude = 3*self.s1.magnitude + 2*self.s2.magnitude

    def update_predecessors(self):
        el = self.father
        while el!= -1:
            el.update_magnitude()
            el = el.father

    def reduce(self):
        action_needed = True
        while action_needed:
            action_needed = False
            for l in self.leaves:
                if action_needed:
                    break
                if l.level == 5:
                    l.father.explode()
                    action_needed = True
            for l in self.leaves:
                if action_needed:
                    break
                if l.magnitude >= 10:
                    l.split()
                    action_needed = True
    
    def explode(self):
        i_1 = self.s1.index_n
        i_2 = self.s2.index_n
        v_1 = self.s1.magnitude
        v_2 = self.s2.magnitude
        if i_1 > 0:
            self.root.leaves[i_1-1].magnitude += v_1
            self.root.leaves[i_1-1].update_predecessors()
        if i_2 < len(self.root.leaves)-1:
            self.root.leaves[i_2 + 1].magnitude += v_2
            self.root.leaves[i_2 + 1].update_predecessors()
        self.magnitude = 0
        self.is_number = True
        self.index_n = i_1
        self.root.leaves[i_1] = self
        self.update_predecessors()
        del self.root.leaves[i_2]
        del self.s1
        del self.s2
        for index in range(i_2, len(self.root.leaves)):
            self.root.leaves[index].index_n = index
        
    def split(self):
        v_1 = self.magnitude//2
        v_2 = self.magnitude - v_1
        i_1 = self.index_n
        i_2 = i_1 + 1
        self.is_number = False 
        self.s1 = Number(str(v_1), self)
        self.s1.magnitude = v_1
        self.s2 = Number(str(v_2), self)
        self.s2.magnitude = v_2
        self.magnitude = 3*self.s1.magnitude + 2*self.s2.magnitude
        self.s1.index_n = i_1
        self.s2.index_n = i_2
        t_leaves = self.root.leaves
        new_leaves = t_leaves[:i_1] + t_leaves[-2:] + t_leaves[i_1+1:-2]
        self.root.leaves = new_leaves
        for index in range(i_2, len(self.root.leaves)):
            self.root.leaves[index].index_n = index

    def final_fix(self):
        for l in self.leaves:
            l.father.update_predecessors()
        

    def __str__(self) -> str:
        if self.is_number:
            return str(self.magnitude)
        else:
            return "[" + str(self.s1) + "," + str(self.s2) + "]"

    def __add__(self, other):
        ans = Number("[" + str(self) + "," +str(other) + "]", -1)
        ans.reduce()
        return ans



first_element = Number(lines[0], -1)
for addendum in lines[1:]:
    first_element = first_element + addendum


first_element.final_fix()
print(first_element.magnitude)