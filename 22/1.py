import sys
import multiprocessing as mp
import tqdm

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

is_in = lambda x, y : x < y[1] and x > y[0]

def seg_intersect(t1, t2):
    part_in = lambda x, y : is_in(x[0], y) or is_in(x[1],y)
    return part_in(t1,t2) or part_in(t2,t1)

class Rectangle:
    def __init__(self, line):
        if isinstance(line, str):
            self.state, other = line.split(" ")
            extremes = other.split(",")
            extremes = [i.split("=")[1] for i in extremes]
            extremes = tuple(tuple(int(i) for i in j.split("..")) for j in extremes)
            self.extremes = tuple((i[0]-.5, i[1]+.5) for i in extremes)
            #fixer = lambda x : min(max(x, -50.5), 50.5)
            #sm_fifty = lambda x : (fixer(x[0]), fixer(x[1]))
            #self.extremes = [sm_fifty(i) for i in  self.extremes]
        else:
            self.extremes = line
            self.state = "off"
    
    def are_intersecting(self, other):
        t_val = [seg_intersect(self.extremes[i], other.extremes[i]) for i in range(3)]
        return all(t_val)

    def is_inside(self, vec):
        return all([is_in(vec[i], self.extremes[i]) for i in range(3)])

    def eventually_getstate(self, other):
        v = [i[0]+.5 for i in self.extremes]
        if other.extremes[0][0] != other.extremes[0][1]:
            if other.is_inside(v): # or self.are_intersecting(other):
                self.state = other.state

    def get_lighted_area(self):
        if self.state == "on":
            seg_c = lambda i : int(self.extremes[i][1] - self.extremes[i][0])
            return seg_c(0)*seg_c(1)*seg_c(2)
        else:
            return 0

    # Not Used
    def split_accordingly(self, other):
        splitpoints = []
        for i in range(3):
            cur_splits = set(self.extremes[i])
            cur_splits.update(other.extremes[i])
            new_el = []
            for j in range(len(cur_splits)-1):
                new_el.append((cur_splits[i], cur_splits[i+1]))
            splitpoints.append(new_el)
        new_cubes = []
        for dx in splitpoints[0]:
            for dy in splitpoints[1]:
                for dz in splitpoints[2]:
                    new_r = Rectangle((dx, dy, dz))
                    point = (dx[0]+.5, dy[0]+.5, dz[0]+.5)
                    if self.is_inside(point):
                        new_r.state = self.state


rectangles = tuple(Rectangle(l) for l in lines)
def point_mk(pos):
    current_rectangle = Rectangle(pos)
    for r in rectangles:
        current_rectangle.eventually_getstate(r)
    return current_rectangle.get_lighted_area()

def main():
    print("Starting")
    pts = [set() for i in range(3)]
    for r in rectangles:
        for i in range(3):
            pts[i].update(r.extremes[i])
    pts = [list(i) for i in pts]
    small_extremes = [[] for i in range(3)]
    for i in range(3):
        pts[i].sort()
        for index in range(len(pts[i])-1):
            small_extremes[i].append((pts[i][index], pts[i][index+1]))
    print("Small extremes computed")
    my_pool = mp.Pool(4)
    
    ans = 0
    print("job creation")
    for dx in tqdm.tqdm(small_extremes[0]):
        jobs = []
        for dy in small_extremes[1]:
            for dz in small_extremes[2]:
                jobs.append(my_pool.apply_async(point_mk, ((dx,dy,dz),)))
        for i in tqdm.tqdm(jobs):
            ans += i.get()
    print(ans)


    return 0

main()