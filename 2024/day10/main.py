#!/usr/bin/env python3

import argparse
from collections import defaultdict


def load(path):
    with open(path, "r") as f:
        data = [[int(x) for x in line.strip()] for line in f]
    return data


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
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield Point(x, y)
    
    def items(self):
        for p in self:
            yield p, self[p]

    def __str__(self):
        return '\n'.join(''.join(str(v) for v in row) for row in self.values)


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


CARDINAL = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]

class Trails(object):
    def __init__(self, grid):
        self.grid = grid
        self.paths = {}

    def navigate(self, location, elevation):
        if location not in self.grid:
            return []
        if self.grid[location] != elevation:
            return []
        if location in self.paths:
            return self.paths[location]
        destinations = set()
        if elevation == 9:
            destinations.add(location)
        else:
            for dir_ in CARDINAL:
                destinations.update(self.navigate(location + dir_, elevation + 1))
        self.paths[location] = destinations
        return destinations

    def rate(self, location, elevation):
        if location not in self.grid:
            return 0
        if self.grid[location] != elevation:
            return 0
        if location in self.paths:
            return self.paths[location]
        paths = 0
        if elevation == 9:
            # return the number of paths that end here
            paths += 1
        else:
            for dir_ in CARDINAL:
                paths += self.rate(location + dir_, elevation + 1)
        self.paths[location] = paths
        return paths


def part1(path):
    grid = Grid(load(path))
    t = Trails(grid)
    heads = {}
    for p, h in grid.items():
        if h == 0:
            heads[p] = t.navigate(p, 0)
    total = 0
    for head, summits in heads.items():
        #print(f'{head}: {len(summits)} - {summits}')
        total += len(summits)
    print(total)


def part2(path):
    grid = Grid(load(path))
    t = Trails(grid)
    heads = {}
    for p, h in grid.items():
        if h == 0:
            heads[p] = t.rate(p, 0)
    total = 0
    for head, rating in heads.items():
        #print(f'{head}: {rating}')
        total += rating
    print(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
