import sys
import math


DEBUG = False


def dprint(*args):
    if not DEBUG:
        return
    print(*args)


def read_file(path):
    with open(path, "r") as f:
        return f.readline().strip()


def greater_than(vals):
    left, right = vals
    return int(left > right)


def less_than(vals):
    left, right = vals
    return int(left < right)


def equal_to(vals):
    left, right = vals
    return int(left == right)


OP_MAP = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: greater_than,
    6: less_than,
    7: equal_to,
}


class Data(object):
    def __init__(self, value):
        dprint(value)
        self.value = []
        for h in value:
            self.value.extend(int(b) for b in "{:04b}".format(int(h, 16)))
        self.idx = 0
        self.versum = 0
    
    def read(self, bitlen):
        value = 0
        for _ in range(bitlen):
            value <<= 1
            value |= self.value[self.idx]
            self.idx += 1
        return value

    def read_literal(self):
        value = 0
        while True:
            last = self.read(1) == 0
            value <<= 4
            value |= self.read(4)
            if last:
                return value

    def read_packet(self):
        ver = self.read(3)
        self.versum += ver
        typ = self.read(3)
        dprint("v: {}, t: {}".format(ver, typ))
        if typ == 4:
            value = self.read_literal()
            dprint('lit:', value)
            return value
        ltid = self.read(1)
        values = []
        if ltid == 0:
            length = self.read(15)
            end = self.idx + length
            dprint('len:', length)
            while self.idx < end:
                values.append(self.read_packet())
        else:
            pak_count = self.read(11)
            dprint('paks:', pak_count)
            for _ in range(pak_count):
                values.append(self.read_packet())
        return OP_MAP[typ](values)


def sample():
    Data('D2FE28').read_packet()
    Data('38006F45291200').read_packet()
    Data('EE00D40C823060').read_packet()
    print(Data('C200B40A82').read_packet())
    print(Data('04005AC33890').read_packet())


if __name__ == "__main__":
    #sample()
    data = Data(read_file(sys.argv[1]))
    part2 = data.read_packet()
    print(data.versum)
    print(part2)
