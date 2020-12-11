import argparse
import re
from collections import OrderedDict
import heapq
import sys


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

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


class Location(object):
    UNOWNED = object()
    ID = 0

    def __init__(self, x, y):
        self.id = Location.ID
        Location.ID += 1
        self.point = Point(x, y)
        # print("{}: own {}".format(self.id, self.point))
        self.ranges = {0: {self.point.tuple}}
        self.areas = {self.point.tuple: 0}
        self.inf = False

    def disown(self, point):
        # print("{}: disown {}".format(self.id, point))
        dist = self.areas.pop(point.tuple)
        self.ranges[dist].remove(point.tuple)

    def claim(self, grid, dist):
        cur_range = set()
        self.ranges[dist] = cur_range
        for edge in self.ranges[dist - 1]:
            edge = Point(*edge)
            for offset in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                p = edge + offset
                if not grid.contains(p):
                    self.inf = True
                    continue
                other = grid.get(p)
                if other is None:
                    # print("{}: claim {}".format(self.id, p))
                    grid.set(p, self)
                    grid.set_elements += 1
                    cur_range.add(p.tuple)
                    self.areas[p.tuple] = dist
                elif other is self or other is Location.UNOWNED:
                    continue
                else:
                    # print("{}: can't claim {} from {}".format(self.id, p, other.id))
                    if other.areas[p.tuple] == dist:
                        other.disown(p)
                        grid.set(p, Location.UNOWNED)


def read_input(path):
    locs = []
    with open(path, "r") as f:
        for line in f:
            # position=< 9,  1> velocity=< 0,  2>
            locs.append(Location(*map(int, re.match(r'(\d+), *(\d+)', line).groups())))
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


def part1(args):
    locs = read_input(args.input)
    grid = BoundedGrid(Bounds([l.point for l in locs]))
    # print_grid(points, bounds)
    for loc in locs:
        grid.set(loc.point, loc)
        grid.set_elements += 1
    d = 0
    while grid.set_elements < grid.bounds.area:
        d += 1
        for loc in locs:
            loc.claim(grid, d)
    max_area = max(len(l.areas) for l in filter(lambda l: not l.inf, locs))
    print(max_area)


def part2(args):
    thresh = 32 if 'test' in args.input else 10000
    locs = read_input(args.input)
    points = [l.point for l in locs]
    bounds = Bounds([l.point for l in locs])
    area = 0
    for x in range(bounds.minx, bounds.maxx + 1):
        for y in range(bounds.miny, bounds.maxy + 1):
            tot_dist = 0
            for loc in points:
                tot_dist += loc.dist(x, y)
                if tot_dist > thresh:
                    break
            if tot_dist < thresh:
                area += 1
    print("{} of {}".format(area, bounds.area))


if args.part2:
    part2(args)
else:
    part1(args)
