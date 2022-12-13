#!/usr/bin/env python3
import argparse
import re
import heapq

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def load(path):
    with open(args.input, "r") as f:
        return [[x for x in s.strip()] for s in f]


class Grid(object):
    def __init__(self, values):
        self.values = []
        for row in values:
            self.values.append(list(row))

    @property
    def width(self):
        return len(self.values[0])

    @property
    def height(self):
        return len(self.values)

    def get(self, point, default=None):
        try:
            return self[point]
        except IndexError:
            return default

    def __str__(self):
        return '\n'.join(''.join(str(v) for v in row) for row in self.values)

    def __getitem__(self, point):
        if point.x < 0 or point.y < 0:
            raise IndexError('nope')
        return self.values[point.y][point.x]

    def __setitem__(self, point, value):
        if point.x < 0 or point.y < 0:
            raise IndexError('nope')
        self.values[point.y][point.x] = value

    def __contains__(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def range(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield Point(x, y)

    def can_move_to(self, source, dest):
        return self[dest] - self[source] <= 1
        
    def adjacent(self, point):
        source = self[point]
        for p in point.neighbors():
            dest = self.get(p)
            if dest and (dest - source <= 1):
                yield p


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

    def __lt__(self, other):
        return self.y < other.y or self.y == other.y and self.x < other.x

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
    
    def neighbors(self):
        yield self.right()
        yield self.down()
        yield self.left()
        yield self.up()

    def up(self, n=1):
        return Point(self.x, self.y - n)

    def down(self, n=1):
        return Point(self.x, self.y + n)

    def left(self, n=1):
        return Point(self.x - n, self.y)

    def right(self, n=1):
        return Point(self.x + n, self.y)

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


def dijkstra(g, start, end):
    inf = float('inf')
    dist = 1  #  all costs are 1 in this problem
    visited = set()
    costs = { start: 0 }
    path = { start: None }
    to_visit = [(0, start)]
    heapq.heapify(to_visit)

    while True:
        path_cost, source = heapq.heappop(to_visit)
        visited.add(source)
        if source == end:
            break
        for neighbor in g.adjacent(source):
            if neighbor in visited:
                continue
            new_cost = costs[source] + dist
            old_cost = costs.get(neighbor, inf)
            if new_cost < old_cost:
                heapq.heappush(to_visit, (new_cost, neighbor))
                costs[neighbor] = new_cost
                path[neighbor] = source

    # return the path cost of the best path to the destination
    # if we wanted the actual path, we would walk path nodes from the dest to the source
    return costs[end]


def build_grid(data):
    g = Grid(data)
    start = None
    end = None
    # Find the start and end
    # translate characters into numeric heights
    for p in g.range():
        c = g[p]
        if c == 'S':
            start = p
            c = 'a'
        elif c == 'E':
            end = p
            c = 'z'
        g[p] = ord(c)
    return g, start, end


def part1(data):
    g, start, end = build_grid(data)
    cost = dijkstra(g, start, end)
    print(cost)


def part2(fname):
    g, start, end = build_grid(data)
    starts = set()
    a = ord('a')
    b = ord('b')
    for p in g.range():
        if g[p] != b:
            continue
        for adj in g.adjacent(p):
            if g[adj] == a:
                starts.add(adj)
    
    best = 0xFFFFFFFF
    for start in starts:
        solution = dijkstra(g, start, end)
        if solution < best:
            best = solution

    print(best)


data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

