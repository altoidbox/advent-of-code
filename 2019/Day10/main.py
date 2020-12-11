import math

FILE = "input.txt"
#FILE = "example1.txt"


def read_file(path):
    with open(path, "r") as f:
        data = list(map(lambda s: s.strip(), f))
    return data


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

    def __getitem__(self, point):
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

    def slope(self, other):
        if other == self:
            return None
        x = other.x - self.x
        y = other.y - self.y
        gcd = math.gcd(x, y)
        return Slope(x // gcd, y // gcd)

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


class Slope(Point):
    PI_OV2 = math.pi / 2

    def value(self):
        if self.x == 0:
            return math.pi if self.y > 0 else 0
        base = Slope.PI_OV2
        if self.x < 0:
            base += math.pi
        return math.atan(self.y / self.x) + base


def generate_slopes(width, height):
    center = Point(0, 0)
    slopes = set()
    for p in Point.range(Point(-width, -height), Point(width, height)):
        if p == center:
            continue
        slopes.add(center.slope(p))
    return slopes


def observe(grid, point):
    observed = set()
    for p in grid.range():
        s = point.slope(p)
        if s is None:
            continue
        if grid[p] == '#':
            observed.add(s)
    return observed


def part1():
    grid = Grid(read_file(FILE))
    best = None
    best_vals = set()
    for p in grid.range():
        if grid[p] != '#':
            continue
        vals = observe(grid, p)
        #print(p, vals)
        if len(vals) > len(best_vals):
            best = p
            best_vals = vals
    print("{} can see {}".format(best, len(best_vals)))
    return grid, best, best_vals


def blast(grid, point, slope):
    while (point := point + slope) in grid:
        if grid[point] == '#':
            grid[point] = '.'
            return point
    return None


def part2():
    grid, best, best_vals = part1()
    ordered_slopes = list(sorted(best_vals, key=lambda s: s.value()))
    blasted = [best]
    while len(blasted) <= 200:
        dead_slopes = set()
        for slope in ordered_slopes:
            if slope in dead_slopes:
                continue
            p = blast(grid, best, slope)
            if p:
                blasted.append(p)
            else:
                dead_slopes.add(slope)
    #print(blasted[1])
    #print(blasted[2])
    #print(blasted[3])
    #print(blasted[10])
    #print(blasted[20])
    #print(blasted[50])
    #print(blasted[100])
    #print(blasted[199])
    #print(blasted[200])
    #print(blasted[201])
    #print(blasted[299])
    print(blasted[200])


def main():
    #part1()
    part2()


if __name__ == "__main__":
    main()
