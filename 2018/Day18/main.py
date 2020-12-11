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
        pass


class Node:
    def __init__(self, state, y, x):
        self.state = state
        self.x = x
        self.y = y
        self.next_state = state
        self.neighbors = []

    def pick_neighbors(self, grid):
        minx = max(self.x-1, 0)
        maxx = min(self.x+1, len(grid[0])-1)
        miny = max(self.y-1, 0)
        maxy = min(self.y+1, len(grid)-1)
        for yi in range(miny, maxy+1):
            for xi in range(minx, maxx+1):
                if yi == self.y and xi == self.x:
                    continue
                self.neighbors.append(grid[yi][xi])

    def has_neighbors(self, state, minimum):
        for n in self.neighbors:
            if n.state == state:
                minimum -= 1
                if minimum == 0:
                    return True
        return False

    def choose_next(self):
        if self.state == '.':
            if self.has_neighbors('|', 3):
                self.next_state = '|'
        elif self.state == '|':
            if self.has_neighbors('#', 3):
                self.next_state = '#'
        elif self.state == '#':
            if not self.has_neighbors('#', 1) or not self.has_neighbors('|', 1):
                self.next_state = '.'


def read_input(path):
    grid = []
    nodes = []
    with open(path, "r") as f:
        for line in f:
            row = []
            for c in line.strip():
                n = Node(c, len(grid), len(row))
                row.append(n)
                nodes.append(n)
            grid.append(row)
    return grid, nodes


def print_grid(grid):
    print('\n'.join(''.join(n.state for n in row) for row in grid))


def part1(args):
    grid,  nodes = read_input(args.input)
    for node in nodes:
        node.pick_neighbors(grid)

    for m in range(1000):
        for node in nodes:
            node.choose_next()
        for node in nodes:
            node.state = node.next_state
        if m >= 1000 - 28:
            counts = {'.': 0, '|': 0, '#': 0}
            for node in nodes:
                counts[node.state] += 1

            print("{}: {} ({})".format(m, counts['|'] * counts['#'], counts))
            # print_grid(grid)


def part2(args):
    grid,  nodes = read_input(args.input)
    for node in nodes:
        node.pick_neighbors(grid)

    solutions = {}

    cycle_start = 535
    cycle_len = 28
    cycle_solutions = []

    for m in range(cycle_start + cycle_len):  # 1000000000
        for node in nodes:
            node.choose_next()
        for node in nodes:
            node.state = node.next_state
        if m >= cycle_start:
            counts = {'.': 0, '|': 0, '#': 0}
            for node in nodes:
                counts[node.state] += 1

            solution = counts['|'] * counts['#']
            print("{}: {} ({})".format(m, solution, counts))
            # if solution in solutions:
            #    print("{}: {} ({})".format(m, solutions[solution], m - solutions[solution]))
            solutions[solution] = m
            cycle_solutions.append(solution)
        # print_grid(grid)
    answer_idx = (1000 - cycle_start - 1) % cycle_len
    print(cycle_solutions[answer_idx])
    answer_idx = (1000000000 - cycle_start - 1) % cycle_len
    print(cycle_solutions[answer_idx])


if args.part2:
    part2(args)
else:
    part1(args)
