#!/usr/bin/env python3

import argparse


def load(path):
    with open(path, "r") as f:
        data = [line.strip() for line in f]
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


class Dir(object):
    keys = ['NW', 'W', 'SW', 'N', 'Z', 'S', 'NE', 'E', 'SE']
    directions = { d: p for d, p in zip(keys, Point.range(Point(-1, -1), Point(1, 1))) }
    directions.pop('Z')
    keys.remove('Z')
    locals().update(directions)


def match(grid, start, dir_, seq):
    cur = start
    try:
        for val in seq:
            if grid[cur] != val:
                return False
            cur += dir_
    except IndexError:
        return False
    return True


def part1(path):
    grid = Grid(load(path))
    count = 0
    for start in grid:
        for k, v in Dir.directions.items():
            if match(grid, start, v, 'XMAS'):
                count += 1
    print(count)


XPOINTS = [Dir.NW, Dir.NE, Dir.SW, Dir.SE]

def xmatch(grid, start):
    if grid[start] != 'A':
        return False
    count = 0
    for offs in XPOINTS:
        cur = start - offs
        count += int(match(grid, cur, offs * 2, 'MS'))
    return count == 2


def part2(path):
    grid = Grid(load(path))
    count = 0
    for start in grid:
        count += int(xmatch(grid, start))
    print(count)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)

if __name__ == '__main__':
    main()
