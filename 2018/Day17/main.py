import argparse
import re
from collections import OrderedDict, deque
import heapq
import sys


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def rrange(end):
    return range(end-1, 0-1, -1)


def y(point):
    return point[0]


def x(point):
    return point[1]


def add_points(left, right):
    return left[0] + right[0], left[1] + right[1]


def make_point(y=y, x=x):
    return y, x


class Bounds(object):
    def __init__(self, points):
        self.minx = min(p[1] for p in points)
        self.maxx = max(p[1] for p in points)
        self.miny = min(p[0] for p in points)
        self.maxy = max(p[0] for p in points)

    def extend(self, point):
        if x(point) > 0:
            self.maxx += x(point)
        elif x(point) < 0:
            self.minx += x(point)
        if y(point) > 0:
            self.maxy += y(point)
        elif y(point) < 0:
            self.miny += y(point)


class BoundedGrid(object):
    def __init__(self, bounds, empty):
        self.bounds = bounds
        self.grid = []
        for _ in range(bounds.maxy - bounds.miny + 1):
            self.grid.append([empty] * (bounds.maxx - bounds.minx + 1))

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def contains(self, point):
        return self.bounds.minx <= x(point) <= self.bounds.maxx and self.bounds.miny <= y(point) <= self.bounds.maxy

    def get(self, point):
        try:
            return self.grid[point[0] - self.bounds.miny][point[1] - self.bounds.minx]
        except IndexError:
            return None

    def set(self, point, item):
        self.grid[point[0] - self.bounds.miny][point[1] - self.bounds.minx] = item


class Game:
    def __init__(self, grid, source):
        self.grid = grid
        self.dripq = deque()
        self.fillq = deque()
        self.dripq.append(make_point(y=grid.bounds.miny, x=x(source)))

    def has_base(self, p):
        c = self.grid.get(add_points(p, (1, 0)))
        return c == '#' or c == '~'

    def drip(self, p):
        while not self.has_base(p):
            c = self.grid.get(p)
            if c == '.':
                self.grid.set(p, '|')
            elif c == '|' or c is None:
                return
            p = add_points(p, (1, 0))
        self.fillq.append(p)

    def fill(self, start):
        p = start
        left_edge = None
        while self.has_base(p):
            c = self.grid.get(p)
            if c == '.':
                self.grid.set(p, '|')
            elif c == '#':
                left_edge = p
                print("left edge:", p)
                break
            p = add_points(p, (0, -1))
        if not left_edge and self.grid.contains(p):
            print("dripping off:", p)
            self.dripq.append(p)
        p = start
        right_edge = None
        while self.has_base(p):
            c = self.grid.get(p)
            if c == '.':
                self.grid.set(p, '|')
            if c == '#':
                right_edge = p
                print("right edge:", p)
                break
            p = add_points(p, (0, 1))
        if not right_edge and self.grid.contains(p):
            print("dripping off:", p)
            self.dripq.append(p)
        if right_edge and left_edge:
            for x in range(left_edge[1] + 1, right_edge[1]):
                self.grid.set(make_point(y=y(start), x=x), '~')
            self.fillq.append(add_points(start, (-1, 0)))

    def flow(self):
        while True:
            # print(self.grid)
            # print()
            if len(self.fillq) > 0:
                self.fill(self.fillq.popleft())
            elif len(self.dripq) > 0:
                self.drip(self.dripq.popleft())
            else:
                break


def read_input(path):
    points = []
    with open(path, "r") as f:
        for line in f:
            match = re.match(r'([xy])=(\d+), ([xy])=(\d+)..(\d+)', line)
            stype = match.group(1)
            sval = int(match.group(2))
            mtype = match.group(3)
            mrange = range(int(match.group(4)), int(match.group(5)) + 1)
            for mval in mrange:
                points.append(make_point(**{stype: sval, mtype: mval}))
    return points


def part1(args):
    spring = make_point(x=500, y=0)
    points = read_input(args.input)
    bounds = Bounds(points)
    bounds.extend(make_point(y=0, x=1))
    bounds.extend(make_point(y=0, x=-1))
    grid = BoundedGrid(bounds, '.')
    for p in points:
        grid.set(p, '#')
    # grid.set(spring, '+')
    Game(grid, spring).flow()
    print(grid)
    moving = 0
    resting = 0
    for row in grid.grid:
        for item in row:
            if item == '|':
                moving += 1
            elif item == '~':
                resting += 1
    print("{} moving + {} resting = {} wet".format(moving, resting, moving + resting))


def part2(args):
    points = read_input(args.input)


if args.part2:
    part2(args)
else:
    part1(args)
