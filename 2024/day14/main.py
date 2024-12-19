#!/usr/bin/env python3

import argparse
import re
from collections import defaultdict


def load(path):
    with open(path, "r") as f:
        data = []
        for line in (line.strip() for line in f):
            m = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
            p = Point(int(m.group(1)), int(m.group(2)))
            v = Point(int(m.group(3)), int(m.group(4)))
            data.append(Robot(p, v))
    return data


class Robot(object):
    def __init__(self, location, velocity):
        self.location = location
        self.velocity = velocity

    def move(self):
        self.location += self.velocity


class Region(object):
    def __init__(self, topleft, botright):
        self.lowx = topleft.x
        self.hix = botright.x
        self.lowy = topleft.y
        self.hiy = botright.y

    def __contains__(self, point):
        return self.lowx <= point.x < self.hix and self.lowy <= point.y < self.hiy

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"({self.lowx}, {self.lowy})-({self.hix}, {self.hiy})"


class Grid(object):
    def __init__(self, w, h):
        self.grid = defaultdict(set)
        self.width = w
        self.height = h
    
    def normalize(self, point):
        point.x %= self.width
        point.y %= self.height

    def add(self, robot):
        self.normalize(robot.location)
        self.grid[robot.location].add(robot)
    
    def move(self):
        old_grid = self.grid
        self.grid = defaultdict(set)
        for loc in old_grid.values():
            for robot in loc:
                robot.move()
                self.add(robot)
    
    def print(self):
        for y in range(self.height):
            line = []
            for x in range(self.height):
                if Point(x, y) in self.grid:
                    line.append('*')
                else:
                    line.append(' ')
            print(''.join(line))
        return '\n'


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


def product(*items):
    res = 1
    for itm in items:
        res *= itm
    return res


def part1(path):
    data = load(path)
    grid = Grid(101, 103)
    [grid.add(r) for r in data]
    for i in range(100):
        grid.move()
    tl = Region(Point(0, 0), Point(grid.width//2, grid.height//2))
    tr = Region(Point(tl.hix+1, 0), Point(grid.width, tl.hiy))
    bl = Region(Point(0, tl.hiy+1), Point(tl.hix, grid.height))
    br = Region(Point(tl.hix+1, tl.hiy+1), Point(grid.width, grid.height))
    regions = [tl, tr, bl, br]
    totals = [0] * len(regions)
    for l, s in grid.grid.items():
        for i, r in enumerate(regions):
            if l in r:
                totals[i] += len(s)
                break
    print(totals)
    print(product(*totals))


def gen(start, offset):
    while True:
        yield start
        start += offset


def inorder(*generators):
    items = []
    while True:
        while len(items) >= len(generators):
            yield items.pop(0)
        for g in generators:
            items.append(next(g))
        items = sorted(items)


def part2(path):
    data = load(path)
    grid = Grid(101, 103)
    [grid.add(r) for r in data]
    i = 0
    # 29, 107, 130
    a = gen(4, 103)
    b = gen(29, 101)
    #stops = [29, 107, 130, 210, 231, 313, 411]
    for stop in inorder(a, b):
        print(f'stop: {stop}')
        while i < stop:
            grid.move()
            i += 1
        while True:
            grid.print()
            print(i)
            data = input().strip()
            if data == '':
                break
            i += 1
            grid.move()
        


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
