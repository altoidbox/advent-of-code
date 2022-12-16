#!/usr/bin/env python3
import argparse
import re
from functools import cmp_to_key

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


class Grid(dict):
    _sentinel = object()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._minx = self._maxx = 0
        self._miny = self._maxy = 0
        self._dirty = False
        self._fixed_size = False

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._dirty = True

    def __setitem__(self, key, value):
        super(Grid, self).__setitem__(key, value)
        self._dirty = True
        return value
    
    def __delitem__(self, key):
        super(Grid, self).__delitem__(key)
        self._dirty = True

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
            for x in range(self.minx, self.maxx + 1):
                line += str(self.get(Point(x, y), '.'))
            lines.append(line)
        return "\n".join(lines)


def load(path):
    data = []
    with open(args.input, "r") as f:
        for line in f:
            rock = []
            for spoint in line.strip().split(' -> '):
                x, y = spoint.split(',')
                rock.append(Point(int(x), int(y)))
            data.append(rock)
    return data


def add_rock(grid, start, end):
    for p in Point.range(start, end):
        grid[p] = '#'


def prepare(data):
    g = Grid()
    for rock in data:
        for i in range(len(rock) - 1):
            add_rock(g, rock[i], rock[i+1])
    return g


DOWN = Point(0, 1)
DOWNLEFT = Point(-1, 1)
DOWNRIGHT = Point(1, 1)
STEPS = [DOWN, DOWNLEFT, DOWNRIGHT]


def drop_sand(grid, point, floor=False):
    if point in grid:
        return False
    while True:
        for step in STEPS:
            next_point = point + step
            if next_point not in grid:
                point = next_point
                break
        else:
            grid[point] = 'O'
            return True
        if not floor and point.y >= grid.maxy:
            return False
        if floor and point.y >= grid.maxy - 1:
            grid[point] = 'O'
            return True



def part1(data):
    g = prepare(data)
    g.fix_size()
    start = Point(500, 0)
    count = 0
    while drop_sand(g, start):
        #print(g)
        count += 1
    print(count)


def part2(data):
    g = prepare(data)
    g[Point(500, g.maxy+2)] = '#'  # floor
    g.fix_size()
    start = Point(500, 0)
    count = 0
    while drop_sand(g, start, True):
        count += 1
    #print(g)
    print(count)


data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

