import argparse
import re
from collections import OrderedDict
import heapq
import sys


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def rrange(end):
    return range(end-1, 0-1, -1)


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.power_level = None
        self.grid_power = None

    def set_serial(self, serial):
        rack_id = self.x + 10
        power_level = rack_id * self.y
        power_level += serial
        power_level *= rack_id
        power_level //= 100
        power_level %= 10
        self.power_level = power_level - 5

    @property
    def gpv(self):
        if self.grid_power is None:
            return -(2**32)
        return self.grid_power

    def get_grid_power(self, grid, size):
        do_y = True
        try:
            p = grid.get(self + (1, 0))
        except IndexError:
            p = None
        if p is None or p.grid_power is None:
            try:
                do_y = False
                p = grid.get(self + (0, 1))
            except IndexError:
                p = None
        grid_power = 0
        if p is None or p.grid_power is None:
            for x in rrange(size):
                for y in rrange(size):
                    p = grid.get(self + (x, y))
                    if p is None:
                        return
                    grid_power += p.power_level
        else:
            grid_power = p.grid_power
            if do_y:
                for y in range(size):
                    grid_power -= grid.get(self + (size, y)).power_level
                    grid_power += grid.get(self + (0, y)).power_level
            else:
                for x in range(size):
                    grid_power -= grid.get(self + (x, size)).power_level
                    grid_power += grid.get(self + (x, 0)).power_level
        self.grid_power = grid_power

    @property
    def tuple(self):
        return self.x, self.y

    def __str__(self):
        return "<{}, {}>".format(self.x, self.y)

    def __repr__(self):
        return "<{}, {}>".format(self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Point):
            x, y = other.x, other.y
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            x, y = other
        else:
            raise ValueError()
        return Point(x + self.x, y + self.y)

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


class Bounds(object):
    def __init__(self, points):
        self.minx = min(p.x for p in points)
        self.maxx = max(p.x for p in points)
        self.miny = min(p.y for p in points)
        self.maxy = max(p.y for p in points)
        w = self.maxx - self.minx + 1
        h = self.maxy - self.miny + 1
        self.area = w * h


class BoundedGrid(object):
    def __init__(self, bounds):
        self.bounds = bounds
        self.grid = []
        for _ in range(bounds.maxx - bounds.minx + 1):
            self.grid.append([None] * (bounds.maxy - bounds.miny + 1))
        self.set_elements = 0

    def contains(self, point):
        return self.bounds.minx <= point.x <= self.bounds.maxx and self.bounds.miny <= point.y <= self.bounds.maxy

    def get(self, point):
        return self.grid[point.x - self.bounds.minx][point.y - self.bounds.miny]

    def set(self, point, item):
        self.grid[point.x - self.bounds.minx][point.y - self.bounds.miny] = item


def read_input(path):
    locs = []
    with open(path, "r") as f:
        pass
    return locs


def print_grid(points, bounds):
    by_row = sorted(points, key=lambda p: (-p.y, -p.x))
    cur = by_row.pop()
    for y in range(bounds.miny, bounds.maxy + 1):
        for x in range(bounds.minx, bounds.maxx + 1):
            if cur.x == x and cur.y == y:
                sys.stdout.write("#")
                try:
                    while cur.x == x and cur.y == y:
                        cur = by_row.pop()
                except IndexError:
                    pass
            else:
                sys.stdout.write(".")
        sys.stdout.write("\n")


def calc_grid_power(points, grid, size):
    for p in points:
        p.grid_power = None
    for y in range(301 - size, 0, -1):
        for x in range(301 - size, 0, -1):
            grid.get(Point(x, y)).get_grid_power(grid, size)
    return max(points, key=lambda p: p.gpv)


def part1(args):
    serial = int(args.input)
    points = []
    grid = BoundedGrid(Bounds([Point(1, 1), Point(300, 300)]))
    for x in range(1, 301):
        for y in range(1, 301):
            p = Point(x, y)
            p.set_serial(serial)
            grid.set(p, p)
            points.append(p)
    # print_grid(points, bounds)
    p = calc_grid_power(points, grid, 3)
    print("{}: {}".format(p, p.gpv))


def part2(args):
    serial = int(args.input)
    points = []
    grid = BoundedGrid(Bounds([Point(1, 1), Point(300, 300)]))
    for x in range(1, 301):
        for y in range(1, 301):
            p = Point(x, y)
            p.set_serial(serial)
            grid.set(p, p)
            points.append(p)
    # print_grid(points, bounds)
    best = (0,)
    for size in range(1, 301):
        p = calc_grid_power(points, grid, size)
        print("{}: {},{},{}".format(p.grid_power, p.x, p.y, size))
        if p.grid_power > best[0]:
            best = (p.grid_power, p.x, p.y, size)
    print("\n{}: {},{},{}".format(*best))


if args.part2:
    part2(args)
else:
    part1(args)
