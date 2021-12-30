from re import I
import sys
import tqdm

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

class Node:
    def __init__(self, content):
        self.content = content
        self.sons = []
        self.fathers = []
    
    def get_z(self):
        return self.content[0]
    
    def update(self, other):
        self.sons.extend(other.sons)
        self.fathers.extend(other.fathers)

class ALU:
    def __init__(self, lns):
        self.code = lns
    
    def set_val(self, val):
        self.val = val
    
    def divide_chunks(self):
        self.chunks = []
        it = 0
        while it + 18 <= len(self.code):
            self.chunks.append(self.code[it:it+18])
            it += 18

    def get_changing_vars(self):
        self.N1 = [int(i[5].split()[2]) for i in self.chunks]
        self.N2 = [int(i[15].split()[2]) for i in self.chunks]
        self.D = [int(i[4].split()[2]) for i in self.chunks]

    def execute(self, lns = -1, my_z = 0):
        it = max(0, lns)
        variables = {'x' : 0, 'y' : 0, 'z' : my_z, 'w' : 0}
        if lns == -1:
            cur_lines = self.code
        else:
            cur_lines = self.chunks[lns]
        for instruction in cur_lines:
            s_i = instruction.split()
            if s_i[0] == 'inp':
                variables[s_i[1]] = int(self.val[it])
                it += 1
            else:
                command, v1, v2 = s_i
                if v2 in variables:
                    v2_val = variables[v2]
                else:
                    v2_val = int(v2)
                if command == "add":
                    variables[v1] += v2_val
                elif command == "mul":
                    variables[v1] *= v2_val
                elif command == "div":
                    variables[v1] = variables[v1]//v2_val
                elif command == "mod":
                    variables[v1] = variables[v1]%v2_val
                elif command == "eql":
                    if variables[v1] == v2_val:
                        variables[v1] = 1
                    else:
                        variables[v1] = 0
            #print(s_i, variables[s_i[1]])
        return(variables)

    def solve_bf(self):
        starting_val = list(str(99999999999999))
        min_val = float('inf')
        min_getter = 0
        valid_spots = [i for i in range(len(self.chunks)) if self.D[i]==26]
        for i in tqdm.tqdm(range(10**len(valid_spots))):
            cur_input = str(i).zfill(len(valid_spots))
            inp = starting_val.copy()
            it = 0
            for i in valid_spots:
                inp[i] = cur_input[it]
                it += 1
            self.val = inp
            result = self.execute()
            if result['z'] < min_val:
                min_val = result['z']
                min_getter = inp
            if self.execute() == 0:
                return inp
        print(min_getter, min_val)
    
    def solve(self):
        starting_z = 0
        for i in range(len(self.chunks)):
            x_killer = starting_z%26 + self.N1[i]
            if x_killer >= 0 and x_killer <= 9:
                if self.D[i]==26:
                    self.val[i] = x_killer
            vars = self.execute(i, starting_z)
            starting_z = vars['z']
            print(vars)
            print(starting_z%26)
        return starting_z

    def valid_zs(self, ch_number, resulting_z):
        previous_zs = []
        if self.D[ch_number] == 26:
            one_more = [resulting_z*26 + i for i in range(26)]
            other_lst = [(resulting_z//26)*26 + i for i in range(26)]
            previous_zs.extend(one_more)
            previous_zs.extend(other_lst)
        else:
            previous_zs.append(resulting_z)
            previous_zs.append(resulting_z//26)
        ans = set()
        for z_old in previous_zs:
            for w in range(10):
                self.val[ch_number] = w
                sym_result = self.execute(ch_number, z_old)
                z_new = sym_result['z']
                if z_new==resulting_z:
                    ans.add(z_old)
                    #print(z_old, w, sym_result)
        return ans
    
    def compute_prev_level(self, level, old_paths):
        new_paths = set()
        for p in tqdm.tqdm(old_paths):
            p_node = self.tree_dict[p]
            new_zs = self.valid_zs(level, p_node.get_z())
            for new_z in new_zs:
                pair = (new_z, level)
                node = Node(pair)
                node.sons.append(p_node)
                if pair in self.tree_dict:
                    self.tree_dict[pair].update(node)
                    node = self.tree_dict[pair]
                else:
                    self.tree_dict[pair] = node
                p_node.fathers.append(node)
                new_paths.add(pair)
        return new_paths

    def compute_paths(self):
        current_paths = [(0,len(self.chunks))]
        self.tree_dict = dict()
        self.tree_dict[current_paths[0]] = Node(current_paths[0])
        current_level = len(self.chunks) - 1
        for iterations in tqdm.tqdm(range(len(self.chunks)-1, -1, -1)):
            new_paths = self.compute_prev_level(current_level, current_paths)
            current_paths = new_paths
            current_level -= 1
        current_element = self.tree_dict[(0,0)]
        for level in range(len(self.chunks)):
            son_vals = [i.get_z() for i in current_element.sons]
            current_z = current_element.get_z()
            for i in range(9,-1,-1):
                self.val[level] = i
                new_z = self.execute(level,current_z)['z']
                if new_z in son_vals:
                    current_element = self.tree_dict[(new_z,level+1)]
                    break
        return "".join([str(i) for i in self.val])



a = ALU(lines)
a.set_val(list("99999999999999"))
a.divide_chunks()
a.get_changing_vars()
#print(a.solve())
ans = a.compute_paths()
print(ans)