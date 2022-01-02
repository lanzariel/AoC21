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
        else:
            self.extremes = line
            self.state = "on"
    
    def is_intersecting(self, other):
        if isinstance(other, tuple):
            return self.is_intersecting(Rectangle(other))
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
        
        
        ans = set()
        for r in others:
            my_pts = [[] for i in range (3)]
            for i in range(3):
                for ex in small_extremes[i]:
                    if r.extremes[i][0] <= ex[0] and r.extremes[i][1] >= ex[1]:
                        my_pts[i].append(ex)
            if r.state == "on":
                for dx in my_pts[0]:
                    for dy in my_pts[1]:
                        for dz in my_pts[2]:
                            ans.add((dx,dy,dz))
            else:
                for dx in my_pts[0]:
                    for dy in my_pts[1]:
                        for dz in my_pts[2]:
                            el = (dx,dy,dz)
                            if el in ans:
                                ans.remove(el)
        return ans


rectangles = tuple(Rectangle(l) for l in lines)
def point_mk(pos):
    current_rectangle = Rectangle(pos)
    for r in rectangles:
        current_rectangle.eventually_getstate(r)
    return current_rectangle.get_lighted_area()

def main():
    processed = set()
    for it in tqdm.tqdm(range(len(rectangles))):
        intersecting = []
        for it_prev in processed:
            if rectangles[it].is_intersecting(Rectangle(it_prev)):
                intersecting.append(it_prev)
        if len(intersecting) == 0 and rectangles[it].state == "on":
            processed.add(rectangles[it].extremes)
        if len(intersecting) > 0:
            logging.debug("Starting Process")
            to_process = [Rectangle(i) for i in intersecting]
            for it_prev in intersecting:
                if it_prev in processed:
                    processed.remove(it_prev)
            logging.debug("New Processed created starting split")
            worked = rectangles[it].split_accordingly(to_process)
            logging.debug("Got Split")
            processed.update(worked)
    ans = 0
    for r in processed:
        ans += Rectangle(r).get_lighted_area()
    print(ans)
    return 0

main()