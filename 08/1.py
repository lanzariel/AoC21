import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]


digiconv = dict()
digiconv[('a', 'b', 'c', 'e', 'f', 'g')] = 0
digiconv[('c', 'f')] = 1
digiconv[('a', 'c', 'd', 'e', 'g')] = 2
digiconv[('a', 'c', 'd', 'f', 'g')] = 3
digiconv[('b', 'c', 'd', 'f')] = 4
digiconv[('a', 'b', 'd', 'f', 'g')] = 5
digiconv[('a', 'b', 'd', 'e', 'f', 'g')] = 6
digiconv[('a', 'c', 'f')] = 7
digiconv[('a', 'b', 'c', 'd', 'e', 'f', 'g')] = 8
digiconv[('a', 'b', 'c', 'd', 'f', 'g')] = 9

a_ord = ord('a')

print("Generating Permutations")
def generate_permutations(lst):
    if len(lst)==1:
        return [lst.copy()]
    real_ans = []
    for i in range(len(lst)):
        reduced_list = lst[:i] + lst[i+1:]
        factor = [[lst[i]] + rest for rest in generate_permutations(reduced_list)] 
        real_ans.extend(factor)
    return real_ans
permutations = generate_permutations([0,1,2,3,4,5,6])
#print(generate_permutations([1,2,3]))
print("Permutations ready")

class Digit:
    def __init__(self, text):
        self.encrypted = list(text)
        self.clear = list(text)
        self.clear.sort()
    
    def is_digit(self):
        return tuple(self.clear) in digiconv
    
    def get_digit(self):
        if self.is_digit():
            return digiconv[tuple(self.clear)]
        else:
            return -1
    
    def decrypt(self, permutation):
        self.clear = list()
        for letter in self.encrypted:
            idx = ord(letter) - a_ord
            new_idx = permutation[idx]
            new_letter = chr(a_ord + new_idx)
            self.clear.append(new_letter)
        self.clear.sort()
    
    def is_spottable(self):
        if len(self.encrypted) in [2,3,4,7]:
            return 1
        else:
            return 0

class LineParse:
    def __init__(self, line):
        before, after = line.split(" | ")
        self.train_list = [Digit(i) for i in before.split()]
        self.test_list = [Digit(i) for i in after.split()]
        self.total_list = self.train_list + self.test_list
    
    def find_good_perms(self, big_perm_set, digit_list):
        ans = []
        for p in big_perm_set:
            is_a_good_p = True
            for d in digit_list:
                d.decrypt(p)
                if not d.is_digit():
                    is_a_good_p = False
                    break
            if is_a_good_p:
                ans.append(p)
        return ans

    def train(self, kind = "total"):
        if kind == "total":
            iter_list = self.total_list
        elif kind == "train":
            iter_list = self.train_list
        self.my_perms = self.find_good_perms(permutations, iter_list)


    def is_solvable(self):
        real_good_perms = self.find_good_perms(self.my_perms, self.train_list)
        if len(real_good_perms)==0:
            return False
        answers = []
        for p in self.my_perms:
            current_digit_list = []
            for d in self.train_list:
                d.decrypt(p)
                current_digit_list.append(d.get_digit())
            answers.append(tuple(current_digit_list))
            for a in answers[1:]:
                if a != answers[0]:
                    return False
            return True

    def sol_a(self):
        ans = 0
        for d in self.test_list:
            if d.is_spottable():
                ans += 1
        return ans

how_many_are_solvable = 0
sol_a = 0
for l in lines:
    my_line = LineParse(l)
    my_line.train()
    sol_a += my_line.sol_a()
    if my_line.is_solvable():
        how_many_are_solvable += 1

print(f'The solution of a) is {sol_a}\n')

print(f'There are {len(lines)} lines.')
print(f'Solvable lines: {how_many_are_solvable}')