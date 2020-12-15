import re

FILE = "input.txt"
# FILE = "example1.txt"
# FILE = "example2.txt"


def read_file(path):
    with open(path, "r") as f:
        return list(line.strip() for line in f)


class Mask(object):
    def __init__(self, bits):
        self.or_mask = 0
        self.and_mask = 0
        for bit in bits:
            self.or_mask <<= 1
            self.and_mask <<= 1
            if bit == '1':
                self.or_mask |= 1
            elif bit == 'X':
                self.and_mask |= 1

    def apply(self, value):
        return (value & self.and_mask) | self.or_mask


def part1():
    data = read_file(FILE)
    mask = Mask('X' * 36)
    mem = {}
    for line in data:
        target, value = line.split(" = ")
        if target == "mask":
            mask = Mask(value)
        else:
            addr = int(re.match(r'mem\[(\d+)]', target).group(1))
            mem[addr] = mask.apply(int(value))
    print(sum(mem.values()))


class DecoderV2(object):
    def __init__(self):
        self.memory = {}
        self.or_mask = 0
        self.float_bit_locs = []

    def set_mask(self, bits):
        self.float_bit_locs = []
        self.or_mask = 0
        for i, bit in enumerate(bits):
            self.or_mask <<= 1
            if bit == '1':
                self.or_mask |= 1
            elif bit == 'X':
                self.float_bit_locs.append(1 << (len(bits) - i - 1))
        # print("O:{:036b}".format(self.or_mask))
        # print(self.float_bit_locs)

    def each_addr(self, address):
        mask = []
        try:
            while True:
                while len(mask) < len(self.float_bit_locs):
                    address &= ~self.float_bit_locs[len(mask)]
                    mask.append(0)
                yield address
                while mask.pop() == 1:
                    pass
                address |= self.float_bit_locs[len(mask)]
                mask.append(1)
        except IndexError:
            return

    def decode(self, address, value):
        for addr in self.each_addr(address | self.or_mask):
            self.memory[addr] = value


def part2():
    data = read_file(FILE)
    decoder = DecoderV2()
    for line in data:
        target, value = line.split(" = ")
        if target == "mask":
            decoder.set_mask(value)
            # print("{} Xs".format(len(list(filter(lambda c: c == 'X', value)))))
        else:
            addr = int(re.match(r'mem\[(\d+)]', target).group(1))
            decoder.decode(addr, int(value))
    print(sum(decoder.memory.values()))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
