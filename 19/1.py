import sys
import numpy as np
import tqdm
import multiprocessing as mp

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

i1 = [1, 0, 0]
i2 = [0, 1, 0]
i3 = [0, 0, 1]

positive_t = [[i1,i2,i3], [i1,i3,i2], [i2,i1,i3],[i2,i3,i1],[i3,i1,i2],[i3,i2,i1]]
sign_changer = []
for i in range(8):
    id = np.identity(3,dtype=int)
    if i&4 > 0:
        id[0][0] = -1
    if i&2 > 0:
        id[1][1] = -1
    if i&1 > 0:
        id[2][2] = -1
    sign_changer.append(id)

transforms = [i.dot(j) for i in sign_changer for j in positive_t if np.linalg.det(i.dot(j))==1]
id = np.identity(3,dtype=int)

class Scanner:
    def __init__(self, number):
        self.number = number
        self.beacons = set()
        self.extra_beacons = set()
        self.transform = id.copy()
        self.shift_v = np.array([0,0,0])

    def add_b(self, b):
        self.beacons.add(b)

    def add_b_from_str(self, b_str):
        x,y,z = [int(i) for i in b_str.split(",")]
        self.add_b((x,y,z))

    def n_of_b(self):
        return len(self.beacons)
    
    def get_copy(self):
        copy = Scanner(self.number)
        copy.beacons = self.beacons
        copy.extra_beacons = self.extra_beacons
        copy.transform = self.transform
        copy.shift_v = self.shift_v
        return copy

    def get_rotated_copy(self, n):
        t = transforms[n]
        ans = self.get_copy()
        t_transform = lambda x : set([tuple(t.dot(i)) for i in x])
        ans.beacons = t_transform(self.beacons)
        ans.extra_beacons = t_transform(self.beacons)
        ans.transform = t.dot(ans.transform)
        ans.shift_v = t.dot(ans.shift_v)
        return ans
    
    def get_rotated_copies(self):
        ans = []
        for n in range(len(transforms)):
            ans.append(self.get_rotated_copy(n))
        return ans
    
    def get_shifted_copy(self, v):
        v = np.array(v)
        ans = self.get_copy()
        ans.shift_v = tuple(self.shift_v + v)
        ans.beacons = set()
        for el in self.beacons:
            new_vec = v + el
            new_t = tuple(new_vec)
            ans.beacons.add(new_t)
        ans.extra_beacons = set()
        for el in self.extra_beacons:
            new_vec = v + el
            new_t = tuple(new_vec)
            ans.extra_beacons.add(new_t)
        return ans
    
    def count_overlaps(self, other_scanner):
        set_of_v = set(other_scanner.beacons)
        return len(self.beacons.intersection(set_of_v))

    def overlap_finder_single(self, scanner_lst):
        for scanner in scanner_lst.get_rotated_copies():
            for b_orig in list(self.beacons)[:-11]:
                for b_dest in list(scanner.beacons)[:-11]:
                    shift_v = np.array(b_orig) - np.array(b_dest)
                    beacons_dest = scanner.get_shifted_copy(shift_v)
                    current_overlaps = self.count_overlaps(beacons_dest)
                    if current_overlaps >= 12:
                        return(beacons_dest)
        return -1

    def overlap_finder(self, group_of_scanners):
        real_group = []
        linked_scanners = []
        my_p = mp.Pool(4)
        jobs = [my_p.apply_async(self.overlap_finder_single, (arg,)) for arg in group_of_scanners]
        my_p.close()
        for i in tqdm.tqdm(jobs):
            got = i.get()
            if got!= -1:
                linked_scanners.append(got)
        return linked_scanners
    
    def process_scanners(self, other_scanners):
        not_processed = list(other_scanners)
        to_process = set([self])
        processed = []
        self.extra_beacons = self.beacons.copy()
        pbar = tqdm.tqdm(total=len(not_processed))
        while len(not_processed) > 0:
            current = to_process.pop()
            neighbors = current.overlap_finder(not_processed)
            for ne in neighbors:
                not_processed = [i for i in not_processed if i.number != ne.number]
                self.extra_beacons.update(ne.beacons)
                to_process.add(ne)
                pbar.update(1)
            processed.append(current)
        pbar.close()
        self.processed = processed

# Reading results 
sc_list = []
it = 0
while it < len(lines):
    if lines[it]=="":
        it += 1
    if lines[it][0:2]=="--":
        current_scanner = Scanner(len(sc_list))
        sc_list.append(current_scanner)
    else:
        current_scanner.add_b_from_str(lines[it])
    it += 1


# Making big map
base = sc_list[0]

base.process_scanners(sc_list[1:])
print(len(base.extra_beacons))