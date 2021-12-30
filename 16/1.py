import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

# Convert to binary by convenience
expected_len = 4*len(lines[0])
bin_str = bin(int(lines[0], 16))[2:].zfill(expected_len)

# Creating some structure 

class Packet:
    def __init__(self, big_str):
        self.version = int(big_str[:3],2)
        self.type = int(big_str[3:6],2)
        if self.type != 4:
            self.sons = []
            self.len_type = int(big_str[6])
            if self.len_type==0:
                self.LenNext = int(big_str[7:22],2)
                other_string = big_str[22:22+self.LenNext]
                self.rest = big_str[22+self.LenNext:]
                while len(other_string)>0:
                    generated_son = Packet(other_string)
                    other_string = generated_son.rest
                    self.sons.append(generated_son)
            elif self.len_type==1:
                self.SonNumber = int(big_str[7:18],2)
                other_string = big_str[18:]
                for i in range(self.SonNumber):
                    generated_son = Packet(other_string)
                    other_string = generated_son.rest
                    self.sons.append(generated_son)
                self.rest = other_string

            else:
                print("Wrong len type ID")
            self.son_vsum = sum([i.son_vsum for i in self.sons])+self.version
        else:
            self.son_vsum = self.version
            self.bin_content = ""
            previous_indicator = '1'
            next_index = 6
            while previous_indicator == '1':
                previous_indicator = big_str[next_index]
                chunk = big_str[next_index+1:next_index+5]
                self.bin_content = self.bin_content + chunk
                next_index += 5
            self.rest = big_str[next_index:]

p = Packet(bin_str)
print(p.son_vsum)