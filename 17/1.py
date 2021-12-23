import sys
import tqdm
import multiprocessing as mp

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

useless, raw_x, raw_y = lines[0].split('=')
raw_x = raw_x[:-3]
x_target = [int(i) for i in raw_x.split("..")]
y_target = [int(i) for i in raw_y.split("..")]

def p_fun(vx, vy):
    class Probe:
        def __init__(self, velocity):
            self.initial_velocity = velocity
            self.max_h = 0
            self.vx = velocity[0]
            self.vy = velocity[1]
            self.x = 0
            self.y = 0
            self.reached = False
        
        def step(self):
            self.x += self.vx
            self.y += self.vy
            self.vy -= 1
            if self.vx != 0:
                versore = -self.vx//abs(self.vx)
                self.vx += versore

        def is_in(self):
            in_x = self.x >= x_target[0] and self.x <= x_target[1]
            in_y = self.y >= y_target[0] and self.y <= y_target[1]
            return in_x and in_y
        
        def could_still_make_it(self):
            if self.vy < 0 and self.y < min(y_target):
                return False
            if self.vx >= 0 and self.x > max(x_target):
                return False
            return True
        
        def fire(self):
            while self.could_still_make_it():
                self.step()
                self.max_h = max(self.y, self.max_h)
                if self.is_in():
                    self.reached = True
                    break
    obj = Probe((vx,vy))
    obj.fire()
    if obj.reached:
        return obj.max_h
    else:
        return -1
def main():
    success = []
    test_x = [-1,0]
    test_y = [-1,0]

    test_x[1] = max(x_target)+2
    test_y[0] = min(y_target)-1
    test_y[1] = 1000
    my_p = mp.Pool(4)
    jobs = [my_p.apply_async(p_fun, (i_vx, i_vy)) for i_vx in range(*test_x) for i_vy in range(*test_y)]
    my_p.close()

    success = []
    for job in tqdm.tqdm(jobs):
        i = job.get()
        if i>0:
            success.append(i)

    print(max([i for i in success]))

main()