import sys
import tqdm
import logging
logging.basicConfig(level=logging.WARNING)

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

is_in = lambda x, y : x < y[1] and x > y[0]

def seg_intersect(t1, t2):
    part_in = lambda x, y : is_in(x[0], y) or is_in(x[1],y)
    return part_in(t1,t2) or part_in(t2,t1) or t2==t1

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
    
    def is_intersecting(self, other):
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

    def split_accordingly(self, others):
        import multiprocessing as mp
        logging.debug("Starting")
        others.append(self)
        pts = [set() for i in range(3)]
        small_extremes = [[] for i in range(3)]
        for i in range(3):
            for r in others:
                pts[i].update(r.extremes[i])
            pts[i] = list(pts[i])
            pts[i].sort()
            for index in range(len(pts[i])-1):
                small_extremes[i].append((pts[i][index], pts[i][index+1]))
        logging.debug("Small extremes computed")
        
        
        ans = []
        #my_pool = mp.Pool(4)
        jobs = []
        def my_fun(a):
            current_rectangle = Rectangle(a)
            for r in others:
                current_rectangle.eventually_getstate(r)
            return current_rectangle

        pbar = tqdm.tqdm(total = len(small_extremes[0])*len(small_extremes[1])*len(small_extremes[2]))
        for dx in small_extremes[0]:
            for dy in small_extremes[1]:
                for dz in small_extremes[2]:
                    jobs.append(my_fun((dx,dy,dz)))
        for i in jobs:
            c_r = i
            if c_r.state == "on":
                ans.append(c_r)
            pbar.update(1)
        pbar.close()
        return ans
        logging.debug("job creation")
        #my_pool = mp.Pool(4)
        # for dx in tqdm.tqdm(small_extremes[0]):
        #     jobs = []
        #     for dy in small_extremes[1]:
        #         for dz in small_extremes[2]:
        #             jobs.append(my_pool.apply_async(point_mk, ((dx,dy,dz),)))
        #     for i in tqdm.tqdm(jobs):
        #         ans += i.get()
        # print(ans)


rectangles = tuple(Rectangle(l) for l in lines)
def point_mk(pos):
    current_rectangle = Rectangle(pos)
    for r in rectangles:
        current_rectangle.eventually_getstate(r)
    return current_rectangle.get_lighted_area()

def main():
    processed = []
    for it in tqdm.tqdm(range(len(rectangles))):
        intersecting = []
        for it_prev in range(len(processed)):
            if rectangles[it].is_intersecting(processed[it_prev]):
                intersecting.append(it_prev)
        if len(intersecting) == 0 and rectangles[it].state == "on":
            processed.append(rectangles[it])
        if len(intersecting) > 0:
            new_processed = []
            to_process = [processed[i] for i in intersecting]
            for it_prev in range(len(processed)):
                if it_prev not in intersecting:
                    new_processed.append(processed[it_prev])
            worked = rectangles[it].split_accordingly(to_process)
            new_processed.extend(worked)
            processed = new_processed
    ans = 0
    for r in processed:
        ans += r.get_lighted_area()
    print(ans)
    return 0

main()