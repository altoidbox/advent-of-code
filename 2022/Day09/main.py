#!/usr/bin/env python3
import argparse
import re
import math

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def load(path):
    data = []
    with open(args.input, "r") as f:
        for line in f:
            dir_, num = line.strip().split(' ')
            data.append((dir_, int(num)))
    return data


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

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._dirty = True

    def __setitem__(self, key, value):
        super(Grid, self).__setitem__(key, value)
        self._dirty = True
        return value

    def setdefault(self, key, default):
        result = self.get(key, self._sentinel)
        if result is self._sentinel:
            self[key] = default
            result = default
        return result

    def dim_size(self, dim):
        if len(self) == 0:
            return 0
        min_, max_ = minmax(self.keys(), key=lambda p: p[dim])
        return max_ - min_ + 1

    def _update_ranges(self):
        if self._dirty:
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

    @property
    def width(self):
        return self.dim_size(0)

    @property
    def height(self):
        return self.dim_size(1)

    @property
    def depth(self):
        return self.dim_size(2)

    def __str__(self):
        lines = []
        for y in range(self.miny, self.maxy+1):
            line = ""
            for x in range(self.minx, self.maxx + 1):
                line += str(self.get(Point(x, y), '.'))
            lines.append(line)
        return "\n".join(lines)


Offsets = {
    'L': Point(-1, 0),
    'U': Point(0, -1), 
    'R': Point(1, 0), 
    'D': Point(0, 1)
}
    

def part1(data):
    visited = set()
    H = Point(0, 0)
    T = Point(0, 0)
    for dir_, num in data:
        move = Offsets[dir_]
        for _ in range(num):
            H += move
            offset = H - T
            if offset.x > 1 or offset.x < -1:
                if offset.y == 0:
                    T += move
                else:
                    T += Point(move.x, offset.y)
            elif offset.y > 1 or offset.y < -1:
                if offset.x == 0:
                    T += move
                else:
                    T += Point(offset.x, move.y)
            visited.add(T)
    print(len(visited))


def minmax(it, key=lambda x: x):
    min_ = max_ = None
    for item in it:
        val = key(item)
        if min_ is None or val < min_:
            min_ = val
        if max_ is None or val > max_:
            max_ = val
    return min_, max_


def graph(points, visited):
    g = Grid()
    for p in visited:
        g[p] = '#'
    g[Point(0, 0)] = 's'
    for i, p in reversed(list(enumerate(points))):
        g[p] = i or 'H'
    return str(g)


def slimit(value, limit):
    if value == 0:
        return value
    absval = abs(value)
    s = value // absval
    return s * min(absval, limit)


def part2(data):
    visited = {Point(0, 0)}
    rope = [Point(0, 0) for _ in range(10)]
    for dir_, num in data:
        for _ in range(num):
            move = Offsets[dir_]
            for i, p in enumerate(rope):
                if i == 0:
                    rope[i] += move
                    continue
                offset = rope[i - 1] - rope[i]
                if abs(offset.x) > 1 or abs(offset.y) > 1:
                    move = Point(slimit(offset.x, 1), slimit(offset.y, 1))
                else:
                    # don't need to move this one, nor the rest of the rope
                    break
                rope[i] += move
                if i == 9:
                    visited.add(rope[i])
    print(graph(rope, visited))
    print(len(visited))
    

data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

