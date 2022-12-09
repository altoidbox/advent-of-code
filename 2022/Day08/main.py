#!/usr/bin/env python3
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def load(path):
    with open(args.input, "r") as f:
        return [[Node(int(x)) for x in s.strip()] for s in f]


class Dir:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class Node(object):
    def __init__(self, value):
        self.value = value
        self.visible = [None] * 4
        self.highest = [-1] * 4
    
    def is_visible(self):
        return any(self.visible)


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
        for y in range(0, self.height):
            for x in range(0, self.width):
                yield Point(x, y)

    def reversed_range(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                yield Point(self.width - x - 1, self.height - y - 1)

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


Offsets = [Point(-1, 0), Point(0, -1), Point(1, 0), Point(0, 1)]


def check_dir(g, p, n, dir_):
    other = g[p + Offsets[dir_]]
    if other.highest[dir_] < n.value:
        n.visible[dir_] = True
        n.highest[dir_] = n.value
    else:
        n.visible[dir_] = False
        n.highest[dir_] = other.highest[dir_]



def part1(data):
    g = Grid(data)
    for p in g.range():
        n = g[p]
        if p.x == 0:
            n.visible[Dir.LEFT] = True
            n.highest[Dir.LEFT] = n.value
        else:
            check_dir(g, p, n, Dir.LEFT)

        if p.y == 0:
            n.visible[Dir.UP] = True
            n.highest[Dir.UP] = n.value
        else:
            check_dir(g, p, n, Dir.UP)
    for p in g.reversed_range():
        n = g[p]
        if p.x == g.width - 1:
            n.visible[Dir.RIGHT] = True
            n.highest[Dir.RIGHT] = n.value
        else:
            check_dir(g, p, n, Dir.RIGHT)

        if p.y == g.height - 1:
            n.visible[Dir.DOWN] = True
            n.highest[Dir.DOWN] = n.value
        else:
            check_dir(g, p, n, Dir.DOWN)
    print(len([p for p in g.range() if g[p].is_visible()]))


def check_dir2(g, p, n, dir_):
    can_see = 1
    otherp = p + Offsets[dir_]
    while otherp is not None:
        other = g[otherp]
        if other.value >= n.value:
            break
        can_see += other.visible[dir_]
        otherp = other.highest[dir_]
    n.visible[dir_] = can_see
    n.highest[dir_] = otherp


def score(node):
    product = 1
    for val in node.visible:
        product *= val
    return product


def part2(data):
    g = Grid(data)
    for p in g.range():
        n = g[p]
        if p.x == 0:
            n.visible[Dir.LEFT] = 0
            n.highest[Dir.LEFT] = None
        else:
            check_dir2(g, p, n, Dir.LEFT)

        if p.y == 0:
            n.visible[Dir.UP] = 0
            n.highest[Dir.UP] = None
        else:
            check_dir2(g, p, n, Dir.UP)
    for p in g.reversed_range():
        n = g[p]
        if p.x == g.width - 1:
            n.visible[Dir.RIGHT] = 0
            n.highest[Dir.RIGHT] = None
        else:
            check_dir2(g, p, n, Dir.RIGHT)

        if p.y == g.height - 1:
            n.visible[Dir.DOWN] = 0
            n.highest[Dir.DOWN] = None
        else:
            check_dir2(g, p, n, Dir.DOWN)
    best = max(g.range(), key=lambda p: score(g[p]))
    print(best, score(g[best]))
    

data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

