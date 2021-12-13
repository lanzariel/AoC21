import sys
path = sys.argv[1]

with open(path, "r") as f:
    lines = [i.strip() for i in f.readlines()]


class Node:
    def __init__(self, parent):
        self.parent = parent

    def set_son(self, son):
        self.son = son

    def set_type(self, tp):
        ans = 0
        if tp == ')':
            ans = 3
        elif tp == ']':
            ans = 57
        elif tp == '}':
            ans = 1197
        elif tp == '>':
            ans = 25137
        else:
            self.type = tp
        return ans

    def scoring(self):
        if self.type == '(':
            return 1
        elif self.type == '[':
            return 2
        elif self.type == '<':
            return 4
        elif self.type == '{':
            return 3
        else:
            return '##'
    
    def closure(self):
        if self.type == '(':
            return ')'
        elif self.type == '[':
            return ']'
        elif self.type == '<':
            return '>'
        elif self.type == '{':
            return '}'
        else:
            return '##'


def process_line(l):
    score = 0
    root = Node(-1)
    addendum = root.set_type(-1)
    tree = [root]
    current_parent = root
    for it in range(len(l)):
        if l[it] == current_parent.closure():
            current_parent = current_parent.parent
        else:
            current_parent.set_son(Node(current_parent))
            current_parent = current_parent.son
            addendum = current_parent.set_type(l[it])
            if addendum > 0:
                return 0
    ans = 0
    while current_parent.type != -1:
        ans = ans*5
        ans += current_parent.scoring()
        current_parent = current_parent.parent
    return ans

score_vec = [process_line(i) for i in lines]
score_pos = [i for i in score_vec if i > 0]
score_pos.sort()



print(score_pos[len(score_pos)//2])


