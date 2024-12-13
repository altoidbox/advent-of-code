#!/usr/bin/env python3

import argparse
from functools import cached_property, cmp_to_key
from collections import defaultdict


def load(path):
    with open(path, "r") as f:
        data = [line.strip() for line in f]
    return data


class Grid(dict):
    def __init__(self, values):
        super().__init__()
        for y, row in enumerate(values):
            for x, v in enumerate(row):
                self[Point(x, y)] = v

    @property
    def width(self):
        return len(self.values[0])

    @property
    def height(self):
        return len(self.values)


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

    def __mul__(self, other):
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        raise ValueError('Wrong type')

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __cmp__(self, other):
        v = self.y - other.y
        if v == 0:
            return self.x - other.x
        return v

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)

    @staticmethod
    def limits(a, b):
        miny, maxy = min(a.y, b.y), max(a.y, b.y) + 1
        minx, maxx = min(a.x, b.x), max(a.x, b.x) + 1
        return (minx, maxx), (miny, maxy)

    @staticmethod
    def range(a, b):
        (minx, maxx), (miny, maxy) = Point.limits(a, b)
        for y in range(miny, maxy):
            changed_row = True
            for x in range(minx, maxx):
                yield Point(x, y), changed_row
                changed_row = False

    @staticmethod
    def yrange(a, b):
        (minx, maxx), (miny, maxy) = Point.limits(a, b)
        for x in range(minx, maxx):
            changed_col = True
            for y in range(miny, maxy):
                yield Point(x, y), changed_col
                changed_col = False
    @property
    def tuple(self):
        return self.x, self.y

    def north(self, n=1):
        return Point(self.x, self.y - n)
    
    def east(self, n=1):
        return Point(self.x + n, self.y)

    def south(self, n=1):
        return Point(self.x, self.y + n)

    def west(self, n=1):
        return Point(self.x - n, self.y)

    def dist(self, x, y=1):
        return abs(self.x - x) + abs(self.y - y)


def minmax(it, key=lambda x: x):
    min_ = max_ = None
    for item in it:
        val = key(item)
        if min_ is None or val < min_:
            min_ = val
        if max_ is None or val > max_:
            max_ = val
    return min_, max_


N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)
CARDINAL = [N, E, S, W]


class Field(object):
    def __init__(self, grid):
        self.grid = grid
        self.point, self.plant = grid.popitem()
        self.region = { self.point }
    
    def build(self):
        for dir_ in CARDINAL:
            self.try_add(self.point + dir_)

    def try_add(self, p):
        if p not in self.grid:
            return
        if self.grid[p] != self.plant:
            return
        del self.grid[p]
        self.region.add(p)
        for dir_ in CARDINAL:
            self.try_add(p + dir_)
    
    @cached_property
    def perimeter(self):
        perim = 0
        for p in self.region:
            for dir_ in CARDINAL:
                if (p + dir_) not in self.region:
                    perim += 1
        return perim
    
    @cached_property
    def area(self):
        return len(self.region)
    
    @cached_property
    def cost(self):
        return self.area * self.perimeter

    @cached_property
    def new_cost(self):
        return self.area * self.sides

    @cached_property
    def sides(self):
        #sorted_points = sorted(self.region, key=cmp_to_key(Point.__cmp__))
        minx, maxx = minmax(self.region, lambda p: p.x)
        miny, maxy = minmax(self.region, lambda p: p.y)
        c1 = Point(minx, miny)
        c2 = Point(maxx, maxy)
        #print(f"{self.plant}")
        sides = 0
        #print(f"{self.plant}: {c1}-{c2}")
        for dir_, ext, rg in [(N, E, Point.range), (S, E, Point.range), (E, S, Point.yrange), (W, S, Point.yrange)]:
            continuing = False
            #prev_p = None
            #start = None
            for p, new_line in rg(c1, c2):
                if new_line and continuing:
                    continuing = False
                    #print(f"Ending Side: {start}-{prev_p} (newline)")
                if continuing and (p not in self.region or (p + dir_) in self.region):
                    # previous edge is on a side with nothing towards dir_
                    # but now we have something, so we are no longer continuing
                    continuing = False
                    #print(f"Ending Side: {start}-{p} ({p + dir_})")
                elif not continuing and (p in self.region and (p + dir_) not in self.region):
                    # previous edge is not on a side, this one starts a new side
                    continuing = True
                    sides += 1
                    #start = p
                    #print(f"Starting Side: {p}")
                else:
                    #print(f"Nothing changes: {p}")
                    pass
                #prev_p = p
            if continuing:
                #print(f"Ending Side: {start}-{prev_p} (oef)")
                pass
        #print(f"{self.plant}: {sides}")
        return sides
                    

    def __repr__(self):
        return f"F({self.plant})={repr(self.region)},p={self.perimeter},a={self.area},c={self.cost}"

    def __str__(self):
        return str(self.region)


def part1(path):
    grid = Grid(load(path))
    groups = []
    while len(grid) > 0:
        f = Field(grid)
        f.build()
        groups.append(f)
    #print(groups)
    total = sum(f.cost for f in groups)
    print(total)


def part2(path):
    grid = Grid(load(path))
    groups = []
    while len(grid) > 0:
        f = Field(grid)
        f.build()
        groups.append(f)
        #print(f'{repr(f)}: {f.sides}')
    total = sum(f.new_cost for f in groups)
    print(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
