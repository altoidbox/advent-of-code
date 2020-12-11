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
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def __str__(self):
        return "<{}, {}>".format(self.x, self.y)

    def __repr__(self):
        return "<{}, {}>".format(self.x, self.y)

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def unmove(self):
        self.x -= self.vx
        self.y -= self.vy


def read_input(path):
    points = []
    with open(path, "r") as f:
        for line in f:
            # position=< 9,  1> velocity=< 0,  2>
            points.append(Point(*map(int, re.match(r'position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>', line).groups())))
    return points


class Bounds(object):
    def __init__(self, points):
        self.minx = min(p.x for p in points)
        self.maxx = max(p.x for p in points)
        self.miny = min(p.y for p in points)
        self.maxy = max(p.y for p in points)

    @property
    def area(self):
        w = self.maxx - self.minx
        h = self.maxy - self.miny
        return w * h


def print_message(points, bounds):
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
    points = read_input(args.input)
    bounds = Bounds(points)
    i = 0
    while True:
        #print_message(points, bounds)
        for p in points:
            p.move()
        new_bounds = Bounds(points)
        if new_bounds.area > bounds.area:
            for p in points:
                p.unmove()

            print_message(points, bounds)
            print(i)
            break
        i += 1
        bounds = new_bounds


def part2(args):
    nodes = read_input(args.input)

    if 'test' in args.input:
        answer = work(nodes, 0, 2)
    else:
        answer = work(nodes, 60, 5)

    print("{}".format(answer))


if args.part2:
    part2(args)
else:
    part1(args)
