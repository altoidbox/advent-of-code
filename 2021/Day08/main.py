
def lmap(f, iter):
    return list(map(f, iter))


CHAR_MAP = {i: chr(ord('a') + i) for i in range(7)}
UNIQ_NUMS = {
    2: 1,
    4: 4,
    3: 7,
    7: 8
}

UNIQ_WIRES = {
    6: 'b',
    4: 'e',
    9: 'f'
}

STD = {
    0: 'abc efg',
    1: '  c  f ',
    2: 'a cde g',
    3: 'a cd fg',
    4: ' bcd f ',
    5: 'ab d fg',
    6: 'ab defg',
    7: 'a c  f ',
    8: 'abcdefg',
    9: 'abcd fg',
}
for i, d in STD.items():
    STD[i] = d.replace(' ', '')
RSTD = { v: k for k, v in STD.items() }


class Display():
    def __init__(self, digits):
        self.digits = [set(d) for d in digits]
        self.wire_map = {}
        self.rwire_map = {}
        self.digi_map = {}
        self.lens = {}
        for d in self.digits:
            self.lens.setdefault(len(d), []).append(d)

    def __getitem__(self, key):
        return RSTD[''.join(sorted(self.wire_map[k] for k in key))]

    def map_wire(self, from_, to):
        self.wire_map[from_] = to
        self.rwire_map[to] = from_

    def find_fixed_len_nums(self):
        for leng, digi in UNIQ_NUMS.items():
            self.digi_map[digi] = self.lens[leng][0]

    def find_fixed_count_wires(self):
        wcounts = {}
        for c in CHAR_MAP.values():
            wcounts[sum(int(c in digi) for digi in self.digits)] = c
        for i, c in UNIQ_WIRES.items():
            self.map_wire(wcounts[i], c)
    
    def deduce_wires(self):
        # have digits 1,4,7,8
        # and wires   b,e,f

        # wire a is in 7, but not 1
        for c in self.digi_map[7]:
            if c not in self.digi_map[1]:
                self.map_wire(c, 'a')
                break
        
        # have f, determine 'c', using 1
        for c in self.digi_map[1]:
            if c not in self.wire_map:
                self.wire_map[c] = 'c'
                break
        
        # determine 'd' using 4
        for c in self.digi_map[4]:
            if c not in self.wire_map:
                self.wire_map[c] = 'd'
                break
        
        # determine 'g', as it is last remaining
        for c in CHAR_MAP.values():
            if c not in self.wire_map:
                self.wire_map[c] = 'g'
                break

    @staticmethod
    def deduce(digits):
        disp = Display(digits)
        disp.find_fixed_len_nums()
        disp.find_fixed_count_wires()
        disp.deduce_wires()
        return disp
            

class Entry():
    def __init__(self, line):
        digits, data = line.rstrip().split(" | ")
        self.digits = digits.split()
        self.data = data.split()
    
    def __str__(self):
        return "{} | {}".format(' '.join(self.digits), ' '.join(self.data))
    
    def p1(self):
        res = sum(int(len(d) in UNIQ_NUMS) for d in self.data)
        #print(self.data, res)
        return res


def read_file(path):
    with open(path, "r") as f:
        return lmap(Entry, f)


def part1(f):
    values = read_file(f)
    print(sum(e.p1() for e in values))


def part2(f):
    values = read_file(f)
    total = 0
    for e in values:
        disp = Display.deduce(e.digits)
        total += int(''.join(str(disp[d]) for d in e.data))
    print(total)


def show_counts():
    for c in CHAR_MAP.values():
        print(c, sum(int(c in digi) for digi in STD.values()))
    for i, d in STD.items():
        print(i, len(d))


def main():
    #part1('sample.txt')
    #part1('input.txt')
    part2('sample.txt')
    part2('input.txt')


if __name__ == "__main__":
    main()
