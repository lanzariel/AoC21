import sys

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [i.strip() for i in f.readlines()]

mask = lines[0]
image = lines[2:]

class Image:
    def __init__(self, mask, image):
        self.mask = mask
        self.image = image
        self.rows = len(image)
        self.cols = len(image[0])
        self.outsider_val = '.'
    
    def get_val(self, row, col):
        if row < 0 or row >= self.rows:
            return self.outsider_val
        if col < 0 or col >= self.cols:
            return self.outsider_val
        return self.image[row][col]
    
    def get_transformed_val(self, row, col):
        binary_n = []
        two_pow = 2**8
        ans = 0
        for it_row in range(row-1, row+2):
            for it_col in range(col-1, col+2):
                cur_val = self.get_val(it_row, it_col)
                binary_n.append(cur_val)
                if cur_val == "#":
                    ans += two_pow
                two_pow = two_pow//2
        return self.mask[ans]
    
    def step(self):
        new_image = []
        for it_row in range(-1, self.rows+1):
            current_row = []
            for it_col in range(-1, self.cols+1):
                current_row.append(self.get_transformed_val(it_row, it_col))
            new_image.append(current_row)

        new_outsider_val = self.get_transformed_val(-2,-2)

        self.image = ["".join(i) for i in new_image]
        self.outsider_val = new_outsider_val
        self.rows += 2
        self.cols += 2
    
    def print_image(self):
        for i in self.image:
            print(i)
        print(self.outsider_val)

    def count_ones(self):
        ans = 0
        for r in self.image:
            for c in r:
                if c == "#":
                    ans += 1
        return ans

my_i = Image(mask, image)
for it in range(50):
    my_i.step()
print(my_i.count_ones())