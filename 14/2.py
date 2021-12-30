import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = f.readlines()

poly = lines[0].strip()
rules = lines[2:]

class SmartPoly:
    def __init__(self, poly, rule):
        self.initial = poly[:2]
        self.end = poly[-2:]
        self.d = dict()
        for i in range(len(poly)-1):
            self.add_pair(poly[i:i+2],1)
        self.rule = dict()
        for r in rule:
            my_r = r.strip()
            couple, mid = my_r.split(" -> ")
            self.rule[couple] = [couple[0]+mid, mid+couple[1]]

    def add_pair(self, pair, n):
        if pair in self.d:
            self.d[pair]+=n
        else:
            self.d[pair]=n
    
    def step(self):
        old_d = self.d
        self.d = dict()
        for key, val in old_d.items():
            if key in self.rule:
                for son in self.rule[key]:
                    self.add_pair(son,val)
            else:
                self.add_pair(key,val)
        if self.initial in self.rule:
            self.initial = self.rule[self.initial][0]
        if self.end in self.rule:
            self.end = self.rule[self.end][1]
    
    def letter_dic(self):
        ans = dict()
        for key,val in self.d.items():
            if key==self.initial:
                print("initial", key)
                if key[0] in ans:
                    ans[key[0]] += 1
                else:
                    ans[key[0]] = 1
            if key==self.end:
                print("final", key)
                if key[1] in ans:
                    ans[key[1]] += 1
                else:
                    ans[key[1]] = 1
            for letter in key:
                if letter in ans:
                    ans[letter] += val
                else:
                    ans[letter] = val
        for el in ans:
            ans[el] = ans[el]/2
        return ans

    def ans_1(self):
        d = self.letter_dic()
        v = d.values()
        return max(v) - min(v)

p = SmartPoly(poly, rules)
for i in range(40):
    p.step()
print(int(p.ans_1()))
