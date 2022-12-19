#!/usr/bin/env python3
import argparse
import re
import math

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def minmax(it, key=lambda x: x):
    min_ = max_ = None
    for item in it:
        val = key(item)
        if min_ is None or val < min_:
            min_ = val
        if max_ is None or val > max_:
            max_ = val
    return min_, max_


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

    def up(self, n=1):
        return Point(self.x, self.y - n)

    def down(self, n=1):
        return Point(self.x, self.y + n)

    def left(self, n=1):
        return Point(self.x - n, self.y)

    def right(self, n=1):
        return Point(self.x + n, self.y)

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


class Grid(dict):
    _sentinel = object()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        inf = float('inf')
        self._minx = inf
        self._maxx = -inf
        self._miny = inf
        self._maxy = -inf
        self._dirty = False
        self._fixed_size = False

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._dirty = True

    def __setitem__(self, key, value):
        super(Grid, self).__setitem__(key, value)
        self._maxx = max(self._maxx, key.x)
        self._minx = min(self._minx, key.x)
        self._maxy = max(self._maxy, key.y)
        self._miny = min(self._miny, key.y)
        return value
    
    def __delitem__(self, key):
        super(Grid, self).__delitem__(key)
        #self._dirty = True

    def setdefault(self, key, default):
        result = self.get(key, self._sentinel)
        if result is self._sentinel:
            self[key] = default
            result = default
        return result

    def fix_size(self):
        self._update_ranges()
        self._fixed_size = True

    def _update_ranges(self):
        if self._dirty and not self._fixed_size:
            self._minx, self._maxx = minmax(self.keys(), key=lambda p: p.x)
            self._miny, self._maxy = minmax(self.keys(), key=lambda p: p.y)
            self._dirty = False

    @property
    def minx(self):
        self._update_ranges()
        return self._minx

    @property
    def maxx(self):
        self._update_ranges()
        return self._maxx

    @property
    def miny(self):
        self._update_ranges()
        return self._miny

    @property
    def maxy(self):
        self._update_ranges()
        return self._maxy

    def __str__(self):
        lines = []
        for y in range(self.miny, self.maxy+1):
            line = ""
            for x in range(self.minx - 1, self.maxx + 2):
                if x < self.minx or x > self.maxx:
                    if y == self.maxy:
                        c = '+'
                    else:
                        c = '|'
                else:
                    c = str(self.get(Point(x, y), '.'))
                line += c
            lines.append(line)
        return "\n".join(lines)


class Shape(object):
    def __init__(self, points):
        self.location = Point(0, 0)
        self.grid = Grid()
        points = list(points)
        for p in points:
            self.grid[p] = '#'
        self._lefts = []
        self._rights = []
        self._downs = []
        for p in points:
            l = p.left()
            r = p.right()
            d = p.down()
            if l not in self.grid:
                self._lefts.append(l)
            if r not in self.grid:
                self._rights.append(r)
            if d not in self.grid:
                self._downs.append(d)
        #print(self.grid)
        #print(self._lefts, self._rights, self._downs)
        self.height = self.grid.maxy + 1 - self.grid.miny
        self.width = self.grid.maxx + 1 - self.grid.minx

    def adjust(self, point):
        if isinstance(point, Point):
            return self.location + point
        for p in point:
            yield self.location + p

    @property
    def points(self):
        return self.adjust(self.grid.keys())

    @property
    def left(self):
        return self.adjust(self._lefts)

    @property
    def right(self):
        return self.adjust(self._rights)

    @property
    def down(self):
        return self.adjust(self._downs)


BAR = Shape(Point.range(Point(0, 0), Point(3, 0)))
PLUS = Shape(list(Point.range(Point(1, 0), Point(1, 2))) + list(Point.range(Point(0, 1), Point(2, 1))))
ELL = Shape(list(Point.range(Point(2, 0), Point(2, 2))) + list(Point.range(Point(0, 2), Point(2, 2))))
LINE = Shape(Point.range(Point(0, 0), Point(0, 3)))
BLOCK = Shape(Point.range(Point(0, 0), Point(1, 1)))

SHAPES = [BAR, PLUS, ELL, LINE, BLOCK]


def load(path):
    with open(args.input, "r") as f:
        return f.read().strip()


def add_points(g, points, c):
    for p in points:
        g[p] = c


def rem_points(g, points):
    for p in points:
        del g[p]


def print_chamber(msg, chamber, shape):
    return
    print(msg)
    add_points(chamber, shape.points, '@')
    print(chamber)
    rem_points(chamber, shape.points)


def sig(g):
    # create a 0-based set of the last 30 rows of data, so we can use it to find a cycle
    miny = g.miny
    return frozenset([Point(p.x, p.y - miny) for p in g.keys() if p.y - miny <= 30])


def simulate(chamber, data, count):
    seen = {}
    cycle_height = 0
    idx = 0
    jetidx = 0
    lr = {
        '<': (Point(-1, 0), lambda s: s.left, lambda s, c: s.location.x <= chamber.minx),
        '>': (Point(1, 0), lambda s: s.right, lambda s, c: s.location.x + s.width > chamber.maxx)
    }
    #for idx in range(count):
    while idx < count:
        shape = SHAPES[idx % len(SHAPES)]
        # Determine the start location
        shape.location = Point(2, chamber.miny - 3 - shape.height)
        # Keep going until it comes to rest
        
        print_chamber('Begin', chamber, shape)
        while True:
            # First, apply jet
            jet = data[jetidx % len(data)]
            jetidx += 1
            can_shift = True
            can_drop = True
            move, dir_points, out_of_bounds = lr[jet]
            if not out_of_bounds(shape, chamber):
                for p in dir_points(shape):
                    if p in chamber:
                        # something blocking
                        can_shift = False
                        break
                if can_shift:
                    shape.location += move
            print_chamber('Jet ' + jet, chamber, shape)
            for p in shape.down:
                #print('d', p)
                if p in chamber:
                    # something blocking
                    can_drop = False
                    break
            if can_drop:
                shape.location += Point(0, 1)
                print_chamber('Drop', chamber, shape)
            else:
                break
        #print('Rest')
        add_points(chamber, shape.points, '#')
        # solution for part 2 from: https://github.com/jonathanpaulson/AdventOfCode/blob/master/2022/17.py
        sigg = (jetidx % len(data), (idx + 1) % len(SHAPES), sig(chamber))
        # We've seen this before. Expect there is a cycle.
        if sigg in seen:
            # load up the index and height when we saw it
            oldidx, oldtop = seen[sigg]
            # calc how much the top has changed
            dy = oldtop - chamber.miny
            # calc how many shapes have dropped
            di = idx - oldidx
            # how many full cycles of this nature are left before we've dropped all the shapes
            cycles = (count - idx) // di
            if cycles:
                print("skipping from", idx, 'to', idx + cycles * di, "adding", cycles * dy)
            # how much height those cycles will add
            cycle_height += cycles * dy
            # how many shapes those cycles will add
            idx += cycles * di
            # we can just keep going by one until the end, without putting all those shapes in, because we'll be at the same point in the cycle either way
        seen[sigg] = (idx, chamber.miny)
        #print(chamber)
        #if (jetidx % len(data)) == 0 and ((idx + 1) % len(SHAPES)) == 0:
        #    break
        idx += 1
    print(-chamber.miny + cycle_height)
    return chamber


def make_chamber():
    chamber = Grid()
    for p in Point.range(Point(0, 0), Point(6, 0)):
        chamber[p] = '-'
    return chamber


def part1(data):
    simulate(make_chamber(), data, 2022)


def part2(data):
    simulate(make_chamber(), data, 1000000000000)
    return
    lcm = math.lcm(len(data), len(SHAPES))
    print(len(SHAPES), len(data), lcm, len(data) * len(SHAPES))
    c = simulate(make_chamber(), data, lcm)
    c = simulate(c, data, lcm)
    c = simulate(c, data, lcm)
    round_height = -c.miny
    #count = 1000000000000
    count = 2022
    height = (count // lcm) * round_height
    c2 = simulate(make_chamber(), data, count % lcm)
    print(height + -c2.miny)
    

data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

