import sys
import time

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

# Positions Side Rooms
# 0 2 4 6
# 1 3 5 7

# Positions Hallway
# 8 9 . 10 . 11 . 12 . 13 14 #

# Letters numbers 
# A 0 1  B 2 3  C 4 5  D 6 7

#  #############
#  #89.0.1.2.34#
#  ###1#3#5#7###
#    #0#2#4#6#
#    #########

neighbors = (
    (1,),
    (0, 9, 10),
    (3,),
    (2, 10, 11),
    (5,),
    (4, 11, 12),
    (7,),
    (6, 12, 13),
    (9,),
    (8, 1, 10,),
    (9, 1, 3, 11),
    (10, 3, 5, 12),
    (11, 5, 7, 13),
    (12, 7 ,14),
    (13,)
)

distances = (
    (1,),
    (1, 2, 2),
    (1,),
    (1, 2, 2),
    (1,),
    (1, 2, 2),
    (1,),
    (1, 2, 2),
    (1,),
    (1, 2, 2,),
    (2, 2, 2, 2),
    (2, 2, 2, 2),
    (2, 2, 2, 2),
    (2, 2 ,1),
    (1,)
)

pos_to_pair = (
    (3, 3),
    (2, 3),
    (3, 5),
    (2, 5),
    (3, 7),
    (2, 7),
    (3, 9),
    (2, 9),
    (1, 1),
    (1, 2),
    (1, 4),
    (1, 6),
    (1, 8),
    (1, 10),
    (1, 11)
)

ind_to_letter = ('A', 'B', 'C', 'D')


class Situation:
    def __init__(self, positions = [0,1,2,3,4,5,6,7]):
        self.positions = positions
        self.distance = 0
        self.sons = []
        self.parents = []
    
    def __str__(self):
        my_lines = []
        my_lines.append(list('#############'))
        my_lines.append(list('#...........#'))
        my_lines.append(list('###.#.#.#.###'))
        my_lines.append(list('  #.#.#.#.#  '))
        my_lines.append(list('  #########  '))
        for index in range(8):
            letter = ind_to_letter[index//2]
            pos = pos_to_pair[self.positions[index]]
            my_lines[pos[0]][pos[1]] = letter
        my_lines = [''.join(i) for i in my_lines]
        return "\n".join(my_lines)


    def get_tuple(self):
        return (*self.positions, self.distance)
    
    def copy(self):
        new_me = Situation(self.positions.copy())
        return new_me

    def get_lines(self, lines):
        r = [[], []]
        r[1] = lines[2].split("#")
        r[0] = lines[3].split("#")
        r[1] = [ord(i) - ord("A") for i in r[1][3:7]]
        r[0] = [ord(i) - ord("A") for i in r[0][1:5]]
        used = [0,0,0,0]
        disp = [0 for i in range(8)]
        for el_it in range(4):
            for i in range(2):
                el = r[i][el_it]
                disp[2*el +used[el]] = 2*el_it + i
                used[el] += 1
        self.positions = disp
    
    def position_reverser(self):
        self.reverse = dict()
        for i in range(8):
            self.reverse[self.positions[i]] = i
    
    def is_done(self, index, starting):
        lower_final_pos = (index//2)*2
        if starting == lower_final_pos:
            return True
        else:
            if starting == (lower_final_pos+1):
                if lower_final_pos in self.reverse:
                    other = self.reverse[lower_final_pos]
                    if (other//2)*2 == lower_final_pos:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
    
    def is_done_all(self):
        return all([self.is_done(i,self.positions[i]) for i in range(8)])
    
    def is_allowed(self, index, destination):
        if destination > 7:
            if self.positions[index] > 7:
                return False
            else:
                return True
        lower_pos = (destination//2)*2
        if (index//2)*2 == lower_pos:
            if destination == lower_pos:
                return True
            else:
                if lower_pos not in self.reverse:
                    return False
                other = self.reverse[lower_pos]
                if (other//2)*2 == lower_pos:
                    return True
                else:
                    return False
        else:
            return False

    def list_reachables(self, index):
        distance_multiplier = 10**(index//2)
        current_pos = self.positions[index]
        reachables = []
        reached = set()
        if self.is_done(index, current_pos):
            return []
        for it in range(len(neighbors[current_pos])):
            n = neighbors[current_pos][it]
            if neighbors[current_pos][it] not in self.reverse:
                n_distance = distance_multiplier * distances[current_pos][it]
                reachables.append((n ,n_distance))
                reached.add(n)
        it = 0
        while(it < len(reachables)):
            for n_it in range(len(neighbors[reachables[it][0]])):
                n = neighbors[reachables[it][0]][n_it]
                if n not in reached and n not in self.reverse:
                    old_distance = reachables[it][1]
                    dif_distance = distance_multiplier * distances[reachables[it][0]][n_it]
                    new_distance = old_distance + dif_distance
                    reachables.append((n, new_distance))
                    reached.add(n)
            it += 1
        reachables = [i for i in reachables if self.is_allowed(index, i[0])]
        return reachables
    
    def list_moves(self):
        ans = []
        for i in range(8):
            reachables = self.list_reachables(i)
            for r in reachables:
                new_son = self.copy()
                new_son.positions[i] = r[0]
                new_son.distance = self.distance + r[1]
                ans.append(new_son)
        return ans
    
    def find_minimum(self):
        self.position_reverser()
        tree_dict = dict()
        tree_dict[self.get_tuple()] = self
        to_process = self.list_moves()
        min_distance = float('inf')
        while len(to_process) > 0:
            current = to_process.pop()
            current.position_reverser()
            #print([i.distance for i in to_process])
            #print(current.distance, min_distance, len(to_process))
            print(current)
            current_t = current.get_tuple()
            if current_t not in tree_dict and current.distance < min_distance:
                tree_dict[current_t] = current
                if current.is_done_all():
                    min_distance = min(current.distance, min_distance)
                else:
                    new_distances = current.list_moves()
                    to_process.extend(new_distances)
                    #print([i.distance for i in new_distances])
                    #print("extending by", len(new_distances))
            time.sleep(1)
        return min_distance


s = Situation()
s.get_lines(lines)
print(s.find_minimum())
