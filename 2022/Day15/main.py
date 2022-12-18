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

    def dist(self, p):
        return abs(self.x - p.x) + abs(self.y - p.y)


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
            m = re.search(r'x=(-?\d+), y=(-?\d+):.*x=(-?\d+), y=(-?\d+)', line)
            sx, sy, bx, by = m.groups()
            data.append((Point(int(sx), int(sy)), Point(int(bx), int(by))))
    return data


def prepare(data):
    g = Grid()
    for s, b in data:
        g[s] = 'S'
        g[b] = 'B'
    return g


def part1(data):
    g = prepare(data)
    #print(g)
    y = 2000000
    isnt = set()
    for s, b in data:
        mdist = s.dist(b)
        disty = abs(s.y - y)
        width = mdist - disty
        if width < 0:
            continue
        left = Point(s.x - width, y)
        right = Point(s.x + width, y)
        for p in Point.range(left, right):
            isnt.add(p)
    for s, b in data:
        isnt.discard(b)
    print(len(isnt))
    #print(sorted(isnt, key=lambda p: p.tuple))


class MultiRange(object):
    def __init__(self, start, end):
        self.ranges = [(start, end)]

    def remove(self, rstart, rend):
        replace = []
        for start, end in self.ranges:
            if rend < start or rstart > end:
                replace.append((start, end))
                continue
            if rstart > start:
                replace.append((start, rstart-1))
            if rend < end:
                replace.append((rend + 1, end))
        self.ranges = replace

    @property
    def empty(self):
        return len(self.ranges) == 0

    def iter(self):
        for start, end in self.ranges:
            for i in range(start, end-1):
                yield i

    def __contains__(self, item):
        for rg in self.ranges:
            if item in rg:
                return True
        return False


def part2(data):
    g = prepare(data)
    # We can probably reduce our y ranges much faster than we do, but this doesn't take *too* long
    max_range = 4000000
    for y in range(max_range):
        cur = MultiRange(0, max_range)
        for s, b in data:
            mdist = s.dist(b)
            disty = abs(s.y - y)
            width = mdist - disty
            if width < 0:
                continue
            cur.remove(s.x - width, s.x + width)
            if cur.empty:
                break
        if not cur.empty:
            break
    print(y, cur.ranges)
    print(cur.ranges[0][0] * 4000000 + y)


data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

