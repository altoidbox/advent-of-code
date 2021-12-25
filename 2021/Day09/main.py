import sys
from math import prod


def read_file(path):
    with open(path, "r") as f:
        return [[int(x) for x in s.strip()] for s in f]


class Grid(object):
    def __init__(self, values):
        self.values = []
        for row in values:
            self.values.append(list(row))

    @property
    def width(self):
        return len(self.values[0])

    @property
    def height(self):
        return len(self.values)

    def get(self, point, default=None):
        try:
            return self[point]
        except IndexError:
            return default

    def __getitem__(self, point):
        if point.x < 0 or point.y < 0:
            raise IndexError('nope')
        return self.values[point.y][point.x]

    def __setitem__(self, point, value):
        self.values[point.y][point.x] = value

    def __contains__(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def range(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield Point(x, y)


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(self.tuple)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)

    @staticmethod
    def range(a, b):
        ystart = min(a.y, b.y)
        ystop = max(a.y, b.y) + 1
        for x in range(min(a.x, b.x), max(a.x, b.x) + 1):
            for y in range(ystart, ystop):
                yield Point(x, y)

    @property
    def tuple(self):
        return self.x, self.y

    def adjacent(self):
        yield self.up(1)
        yield self.right(1)
        yield self.down(1)
        yield self.left(1)

    def up(self, n):
        return Point(self.x, self.y - n)

    def down(self, n):
        return Point(self.x, self.y + n)

    def left(self, n):
        return Point(self.x - n, self.y)

    def right(self, n):
        return Point(self.x + n, self.y)

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


def part1(fname):
    g = Grid(read_file(fname))
    total = 0
    lows = []

    for p in g.range():
        cur = g[p]

        for adj in p.adjacent():
            if g.get(adj, 10) <= cur:
                break
        else:
            total += 1 + cur
            lows.append(p)
    print(total)
    return lows


def replace_set(g, set1, set2):
    if len(set1) < len(set2):
        to = set1
        fro = set2
    else:
        to = set2
        fro = set1
    for p in fro:
        g[p][1] = to
        to.add(p)
    return to


def part2(fname):
    default = [9, None]
    g = Grid(read_file(fname))
    
    for p in g.range():
        basin = None
        cur = g[p]
        if cur == 9:
            g[p] = [cur, None]
            continue
        left = g.get(p.left(1), default)[1]
        up = g.get(p.up(1), default)[1]
        if left is None and up is None:
            basin = set()
        elif left is None:
            basin = up
        elif up is None:
            basin = left
        elif left is up:
            basin = left
        else:
            basin = replace_set(g, left, up)
        basin.add(p)
        g[p] = [cur, basin]
    sets = sorted((g[p][1] for p in part1(fname)), key=len, reverse=True)[:3]
    print(' * '.join(str(len(s)) for s in sets), '=', prod(len(s) for s in sets))


if __name__ == "__main__":
    part2(sys.argv[1])
