import sys


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

    def __str__(self):
        return '\n'.join(''.join(str(v) for v in row) for row in self.values)

    def __getitem__(self, point):
        if point.x < 0 or point.y < 0:
            raise IndexError('nope')
        return self.values[point.y][point.x]

    def __setitem__(self, point, value):
        if point.x < 0 or point.y < 0:
            raise IndexError('nope')
        self.values[point.y][point.x] = value

    def __contains__(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def range(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield Point(x, y)

    def adjacent(self, point):
        lower_point = Point(max(0, point.x - 1), max(0, point.y - 1))
        upper_point = Point(min(self.width - 1, point.x + 1), min(self.height - 1, point.y + 1))
        for p in Point.range(lower_point, upper_point):
            if p.x == point.x and p.y == point.y:
                continue
            yield p


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


def energize(g, p, s):
    value = g[p] + 1
    if value > 9:
        s.add(p)
        value = 0
    g[p] = value


def do_round(g):
    new_lit = set()
    for p in g.range():
        energize(g, p, new_lit)
    lit = new_lit
    while new_lit:
        to_process = new_lit
        new_lit = set()
        for p in to_process:
            for adj in g.adjacent(p):
                if adj in lit or adj in new_lit:
                    continue
                energize(g, adj, new_lit)
        lit.update(new_lit)
    return len(lit)


def part1(fname):
    g = Grid(read_file(fname))
    total = 0
    #print(g)
    for i in range(100):
        sz = do_round(g)
        #print(i, sz)
        #print(g)
        total += sz
    print(total)


def part2(fname):
    g = Grid(read_file(fname))
    rnd = 0
    sz = 0
    target = g.width * g.height
    while sz != target:
        sz = do_round(g)
        rnd += 1

    print(rnd)


if __name__ == "__main__":
    #part1(sys.argv[1])
    part2(sys.argv[1])
