import sys


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __mod__(self, other):
        return Point(self.x % other.x, self.y % other.y)
    
    def addmod(self, other, mod):
        return Point((self.x + other.x) % mod.x, (self.y + other.y) % mod.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.y < other.y or self.y == other.y and self.x < other.x

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)


def read_file(fname):
    herds = {
        '>': set(),
        'v': set(),
        '.': set()
    }
    
    with open(fname, 'r') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.strip()):
                last = Point(x, y)
                herds[c].add(last)
    return herds, last + Point(1, 1)


def make_moves(herd, clear, direction, limits):
    move_from = set()
    move_to = set()
    for cuc in herd:
        to = cuc.addmod(direction, limits)
        if to in clear:
            move_from.add(cuc)
            move_to.add(to)
    herd.difference_update(move_from)
    herd.update(move_to)
    clear.difference_update(move_to)
    clear.update(move_from)
    return len(move_to)


def part1(fname):
    herds, limits = read_file(fname)
    east = Point(1, 0)
    south = Point(0, 1)

    rounds = 0
    moves = 1
    while moves:
        rounds += 1
        moves = 0
        moves += make_moves(herds['>'], herds['.'], east, limits)
        moves += make_moves(herds['v'], herds['.'], south, limits)
    print(rounds)


if __name__ == "__main__":
    part1(sys.argv[1])
