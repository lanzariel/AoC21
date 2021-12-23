import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = f.readlines()

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
            self.magnitude = 3*self.s1.magnitude + 2*self.s2.magnitude
        else:
            self.is_number = True
            self.magnitude = int(string[0])
            self.rest = string[1:]
            self.index_n = len(self.root.leaves)
            self.root.leaves.append(self)
    
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
        if i_2 < len(self.root.leaves)-1:
            self.root.leaves[i_2 + 1] += v_2
        self.magnitude = 0
        self.is_number = True
        self.index_n = i_1
        self.root.leaves[i_1] = self
        del self.root.leaves[i_2]
        del self.s1
        del self.s2
        
    def split(self):
        v_1 = self.magnitude//2
        v_2 = self.magnitude - v_1
        i_1 = self.index_n
        i_2 = i_1 + 1
        self.is_number = False 
        self.s1 = Number(str(v_1), self)
        self.s2 = Number(str(v_2), self)
        self.s1.index_n = i_1
        self.s2.index_n = i_2

        

    def __str__(self) -> str:
        if self.is_number:
            return str(self.magnitude)
        else:
            return "[" + str(self.s1) + "," + str(self.s2) + "]"



n1 = Number("[[[[4,3],4],4],[7,[[8,4],9]]]", -1)
n2 = Number("[1,1]", -1)
n3 = Number("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", -1)

print(n3.magnitude)
print(n3)

#print(n1 + n2)