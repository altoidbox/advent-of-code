#!/usr/bin/env python3
import argparse
import re
import functools

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


@functools.total_ordering
class Point3D(object):
    def __init__(self, *dims):
        self.dims = list(dims)
        self._tuple = None

    def copy(self):
        return Point(*self.dims)

    @property
    def x(self):
        return self.dims[0]

    @x.setter
    def x(self, value):
        self.dims[0] = value
        self._tuple = None

    @property
    def y(self):
        return self.dims[1]

    @y.setter
    def y(self, value):
        self.dims[1] = value
        self._tuple = None

    @property
    def z(self):
        return self.dims[2]

    @z.setter
    def z(self, value):
        self.dims[2] = value
        self._tuple = None

    @property
    def tuple(self):
        # returning it like this makes it sort naturally as a tuple
        if not self._tuple:
            self._tuple = tuple(reversed(self.dims))
        return self._tuple

    def dist(self, other):
        return sum(abs(s - o) for s, o in zip(self.dims, other.dims))

    def rotate(self, x, y, z):
        p = Point(*self.dims)
        for _ in range(x % 4):
            tz = p.y
            p.y = -p.z
            p.z = tz
        for _ in range(y % 4):
            tx = p.z
            p.z = -p.x
            p.x = tx
        for _ in range(z % 4):
            ty = p.x
            p.x = -p.y
            p.y = ty
        return p

    def __getitem__(self, item):
        return self.dims[item]

    def __setitem__(self, key, value):
        self.dims[key] = value

    def __hash__(self):
        return hash(self.tuple)

    def __add__(self, other):
        return Point3D(*(s + o for s, o in zip(self.dims, other.dims)))

    def __sub__(self, other):
        return Point3D(*(s - o for s, o in zip(self.dims, other.dims)))

    def __neg__(self):
        return Point3D(*(-d for d in self.dims))
    
    def __mul__(self, other):
        return Point3D(*(s * o for s, o in zip(self.dims, other.dims)))

    def __eq__(self, other):
        return self.tuple == other.tuple

    def __lt__(self, other):
        return self.tuple < other.tuple

    def __str__(self):
        return "({})".format(",".join(str(d) for d in self.dims))

    def __repr__(self):
        return "Point3D({})".format(",".join(str(d) for d in self.dims))

    def adjacent6(self):
        for x in range(-1, 1 + 1, 2):
            yield self + Point3D(x, 0, 0)
        for y in range(-1, 1 + 1, 2):
            yield self + Point3D(0, y, 0)
        for z in range(-1, 1 + 1, 2):
            yield self + Point3D(0, 0, z)

    def adjacent(self):
        for x in range(-1, 1 + 1):
            for y in range(-1, 1 + 1):
                for z in range(-1, 1 + 1):
                    if 0 == x == y == z:
                        continue
                    yield self + Point3D(x, y, z)

    @staticmethod
    def range3(start, end):
        for x in range(start.x, end.x + 1):
            for y in range(start.y, end.y + 1):
                for z in range(start.z, end.z + 1):
                    yield Point3D(x, y, z)


def minmax(it, key=lambda x: x):
    min_ = max_ = None
    for item in it:
        val = key(item)
        if min_ is None or val < min_:
            min_ = val
        if max_ is None or val > max_:
            max_ = val
    return min_, max_


def load(path):
    grid = set()
    with open(args.input, "r") as f:
        for line in f:
            grid.add(Point3D(*(int(n) for n in line.strip().split(','))))
    return grid


def part1(data):
    area = 0
    for point in data:
        for edge in point.adjacent6():
            if edge not in data:
                area += 1
    print(area)


def part2(data):
    minx, maxx = minmax(data, key=lambda p: p.x)
    miny, maxy = minmax(data, key=lambda p: p.y)
    minz, maxz = minmax(data, key=lambda p: p.z)
    minp = Point3D(minx-1, miny-1, minz-1)
    maxp = Point3D(maxx+1, maxy+1, maxz+1)

    area = 0
    visited = set()
    to_visit = set()
    to_visit.add(minp)
    while to_visit:
        cur = to_visit.pop()
        visited.add(cur)
        for adj in cur.adjacent6():
            if adj in data:
                area += 1
            elif adj not in visited:
                if not minp.x <= adj.x <= maxp.x:
                    continue
                if not minp.y <= adj.y <= maxp.y:
                    continue
                if not minp.z <= adj.z <= maxp.z:
                    continue
                to_visit.add(adj)
    print(area)

data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

