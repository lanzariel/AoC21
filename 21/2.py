import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

class Die:
    def __init__(self):
        self.value = 0
        self.thrown = 0
    def throw(self):
        self.value = self.value % 100
        self.value += 1
        self.thrown += 1
        return self.value

class DynamicProgram:
    def __init__(self, dice_size, winning_tresh):
        self.dice_size = dice_size
        self.winning_tresh = winning_tresh

        self.dp = []
        zeromat = lambda x : [[0 for i in range(x)] for j in range(x)]
        dzeromat = lambda x : [zeromat(x) for i in range(2)]
        self.dp = [[dzeromat(winning_tresh)for j in range(10)] for i in range(10)]

        self.how_many_there = dict()
        for i in range(dice_size):
            for j in range(dice_size):
                for k in range(dice_size):
                    s = i + j + k + 3
                    if s in self.how_many_there:
                        self.how_many_there[s] += 1
                    else:
                        self.how_many_there[s] = 1
    
    def get(self, p1, p2, turn, s1, s2):
        if s1 >= self.winning_tresh:
            return (1,0)
        if s2 >= self.winning_tresh:
            return (0,1)
        return self.dp[p1][p2][turn][s1][s2]

    def compute(self, p1, p2, turn, s1, s2):
        next_turn = (turn + 1) % 2
        ans = (0,0)
        for k in self.how_many_there:
            if turn==0:
                new_p1 = (p1 + k) % 10
                new_s1 = s1 + new_p1 + 1
                new_winning = self.get(new_p1, p2, 1-turn, new_s1, s2)
            else:
                new_p2 = (p2 + k) % 10
                new_s2 = s2 + new_p2 + 1
                new_winning = self.get(p1, new_p2, 1-turn, s1, new_s2)
            to_add = tuple(i*self.how_many_there[k] for i in new_winning)
            ans = tuple(ans[i] + to_add[i] for i in range(2))
        return ans

    def compute_t_s(self, s1, s2):
        for p1 in range(10):
            for p2 in range(10):
                for turn in range(2):
                    val = self.compute(p1, p2, turn, s1, s2)
                    self.dp[p1][p2][turn][s1][s2] = val

    def compute_solve(self):
        high_v = self.winning_tresh
        for total in range(2*high_v-2, -1, -1):
            for x in range(max(total-high_v+1,0), min(total+1,high_v)):
                y = total - x
                self.compute_t_s(x,y)

    def get_solution(self, ln):
        get_start = lambda x : int(x.split(": ")[1])
        p1, p2 = [get_start(i) for i in ln]
        return self.get(p1-1,p2-1,0,0,0)


g = DynamicProgram(3,21)
g.compute_solve()
print(max(g.get_solution(lines)))

    