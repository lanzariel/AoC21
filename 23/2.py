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


#  #############
#  #67.8.9.0.12#
#  ###3#7#1#5###
#    #2#6#0#4#
#    #1#5#9#3#
#    #0#4#8#2#
#    #########


neighbors = (
    (1,),           #0
    (0, 2),
    (1, 3),
    (2, 17, 18),
    (5,),           #4
    (4, 6),
    (5, 7),
    (6, 18, 19),
    (9,),           #8
    (8, 10),
    (9, 11),
    (10, 19, 20),
    (13,),           #12
    (12, 14),
    (13, 15),
    (14, 20, 21),
    (17,),          #16
    (16, 3, 18,),
    (17, 3, 7, 19),
    (18, 7, 11, 20),
    (19, 11, 15, 21), #20
    (20, 15 ,22),
    (21,)
)

distances = (
    (1,),           #0
    (1, 1),
    (1, 1),
    (1, 2, 2),
    (1,),           #4
    (1, 1),
    (1, 1),
    (1, 2, 2),
    (1,),           #8
    (1, 1),
    (1, 1),
    (1, 2, 2),
    (1,),           #12
    (1, 1),
    (1, 1),
    (1, 2, 2),
    (1,),           #16
    (1, 2, 2,),
    (2, 2, 2, 2),
    (2, 2, 2, 2),
    (2, 2, 2, 2),   #20
    (2, 2 ,1),
    (1,)
)

pos_to_pair = (
    (5, 3),     #0
    (4, 3),
    (3, 3),
    (2, 3),
    (5, 5),     #4
    (4, 5),
    (3, 5),
    (2, 5),
    (5, 7),     #8
    (4, 7),
    (3, 7),
    (2, 7),
    (5, 9),     #12
    (4, 9),
    (3, 9),
    (2, 9),
    (1, 1),     #16
    (1, 2),
    (1, 4),
    (1, 6),
    (1, 8),     #20
    (1, 10),
    (1, 11)
)

ind_to_letter = ('A', 'B', 'C', 'D')


class Situation:
    def __init__(self, positions = list(range(16))):
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
        my_lines.append(list('  #.#.#.#.#  '))
        my_lines.append(list('  #.#.#.#.#  '))
        my_lines.append(list('  #########  '))
        for index in range(16):
            letter = ind_to_letter[index//4]
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
        r = [[], [], [], []]
        r[3] = lines[2].split("#")
        r[2] = lines[3].split("#")
        r[1] = lines[4].split("#")
        r[0] = lines[5].split("#")
        r[3] = [ord(i) - ord("A") for i in r[3][3:7]]
        r[2] = [ord(i) - ord("A") for i in r[2][1:5]]
        r[1] = [ord(i) - ord("A") for i in r[1][1:5]]
        r[0] = [ord(i) - ord("A") for i in r[0][1:5]]
        used = [0,0,0,0]
        disp = [0 for i in range(16)]
        for el_it in range(4):
            for i in range(4):
                el = r[i][el_it]
                disp[4*el +used[el]] = 4*el_it + i
                used[el] += 1
        self.positions = disp
    
    def position_reverser(self):
        self.reverse = dict()
        for i in range(16):
            self.reverse[self.positions[i]] = i
    
    def is_done(self, index, starting):
        lower_final_pos = (index//4)*4
        if starting == lower_final_pos:
            return True
        else:
            if (starting//4)*4 == lower_final_pos:
                if all([i in self.reverse for i in range(lower_final_pos, starting)]):
                    other = [self.reverse[i] for i in range(lower_final_pos, starting)]
                    if all([(i//4)*4 == lower_final_pos for i in other]):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
    
    def is_done_all(self):
        return all([self.is_done(i,self.positions[i]) for i in range(16)])
    
    def is_allowed(self, index, destination):
        if destination > 15:
            if self.positions[index] > 15:
                return False
            else:
                return True
        lower_pos = (destination//4)*4
        if (index//4)*4 == lower_pos:
            if destination == lower_pos:
                return True
            else:
                if any([i not in self.reverse for i in range(lower_pos,destination)]):
                    return False
                other = [self.reverse[i] for i in range(lower_pos,destination)]
                if all([(i//4)*4 == lower_pos for i in other]):
                    return True
                else:
                    return False
        else:
            return False

    def list_reachables(self, index):
        distance_multiplier = 10**(index//4)
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
        for i in range(16):
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
            #print(current)
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
            #time.sleep(1)
        return min_distance


s = Situation()
nl_1 = ["  #D#C#B#A#"]
nl_2 = ["  #D#B#A#C#"]
new_lines = lines[:3] + nl_1 +nl_2 + lines[3:]
s.get_lines(new_lines)
print(s.find_minimum())
