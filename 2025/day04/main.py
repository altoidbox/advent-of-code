#!/usr/bin/env python3

import argparse
from functools import total_ordering


def readlines_stripped(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data


@total_ordering
class Point(object):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

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
    
    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)
    
    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)
    
    def __iter__(self):
        return iter(self.tuple) 

    @staticmethod
    def limits(a, b):
        miny, maxy = min(a.y, b.y), max(a.y, b.y) + 1
        minx, maxx = min(a.x, b.x), max(a.x, b.x) + 1
        return Point(minx, maxx), Point(miny, maxy)
    
    @staticmethod
    def range(a, b):
        (minx, maxx), (miny, maxy) = Point.limits(a, b)
        for y in range(miny, maxy):
            for x in range(minx, maxx):
                yield Point(x, y)

    @property
    def tuple(self):
        return self.x, self.y

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Grid(object):
    def __init__(self, values):
        self.values = []
        for row in values:
            self.values.append(list(row))

    def copy(self):
        return Grid([row.copy() for row in self.values])

    @property
    def width(self):
        return len(self.values[0])

    @property
    def height(self):
        return len(self.values)

    def get(self, point, default=None):
        if point not in self:
            return default
        return self.values[point.y][point.x]

    def __getitem__(self, point):
        if point not in self:
            raise IndexError(f'Out of bounds: {point}')
        return self.values[point.y][point.x]

    def __setitem__(self, point, value):
        if point not in self:
            raise IndexError(f'Out of bounds: {point}')
        self.values[point.y][point.x] = value

    def __contains__(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def __iter__(self):
        for y in range(0, self.width):
            for x in range(0, self.height):
                yield Point(x, y)
    
    def items(self):
        for p in self:
            yield p, self[p]

    def __str__(self):
        return '\n'.join(''.join(str(v) for v in row) for row in self.values)


def load(path):
    return Grid(readlines_stripped(path))


def surrounding(point: Point):
    for p in Point.range(point - Point(1, 1), point + Point(1, 1)):
        if p != point:
            yield p


def part1(path):
    grid = load(path)
    accessible = 0
    for point in grid:
        if grid[point] != '@':
            continue
        count = 0
        for p in surrounding(point):
            if grid.get(p) == '@':
                count += 1
        if count < 4:
            accessible += 1
    print(accessible)


def part2(path):
    grid = load(path)
    removed = 0
    changed = True
    while changed:
        changed = False
        for point in grid:
            if grid[point] != '@':
                continue
            count = 0
            for p in surrounding(point):
                if grid.get(p) == '@':
                    count += 1
            if count < 4:
                removed += 1
                grid[point] = 'x'
                changed = True
    print(removed)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
