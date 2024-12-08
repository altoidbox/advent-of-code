#!/usr/bin/env python3

import argparse
from collections import defaultdict


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
    #print(directions)
    for ignored in ['NW', 'SW', 'NE', 'SE', 'Z']:
        directions.pop(ignored)
        keys.remove(ignored)
    locals().update(directions)

    right_rotations = { N: E, E: S, S: W, W: N }
    left_rotations = { v: k for k, v in right_rotations.items() }
    chr_to_dir = { '^': N, '>': E, 'v': S, '<': W }
    dir_do_chr = { v: k for k, v in chr_to_dir.items() }
    
    @staticmethod
    def rot_right(dir_:Point):
        return Dir.right_rotations[dir_]
    
    @staticmethod
    def rot_left(dir_:Point):
        return Dir.left_rotations[dir_]


class Guard(object):
    def __init__(self, grid:Grid):
        self.grid = grid
        self.walls = set()
        self.location = None
        self.direction = None
        self.analyze()
    
    def analyze(self):
        for p, chr in self.grid.items():
            if chr == '.':
                continue
            elif chr == '#':
                self.walls.add(p)
            elif chr in Dir.chr_to_dir:
                if self.location is not None:
                    raise(f'second location: {p}: {chr} ({self.location}: {self.direction})')
                self.location = p
                self.direction = Dir.chr_to_dir[chr]
            else:
                raise(f'bad chr: {p}: {chr}')
        if self.location is None:
            raise(f'no start found')

    def move(self):
        front_pos = self.location + self.direction
        if front_pos in self.walls:
            self.direction = Dir.rot_right(self.direction)
        else:
            self.location = front_pos


def part1(path):
    grid = Grid(load(path))
    guard = Guard(grid)
    positions = set()
    while guard.location in grid:
        positions.add(guard.location)
        guard.move()
    print(len(positions))


class WallGrid(object):
    """
    Incomplete, but the idea would be to maintain an array of the walls in every row
    and an array of the walls in every column. This way instead of moving one cell at
    a time, we could just move to the next wall immediately (or, off the grid if no 
    wall exists further in the same direction)
    """
    def __init__(self, grid: Grid):
        self.rows = []
        self.cols = []
        for x in range(grid.width):
            pass


def find_loop(guard):
    history = defaultdict(set)
    while guard.location in guard.grid:
        if guard.direction in history[guard.location]:
            return True
        history[guard.location].add(guard.direction)
        guard.move()
    return False


def part2(path):
    grid = Grid(load(path))
    guard = Guard(grid)
    positions = set()
    candidates = []
    while guard.location in guard.grid:
        wall_pos = guard.location + guard.direction
        if wall_pos not in positions and wall_pos in grid and wall_pos not in guard.walls:
            loc, dir_ = guard.location, guard.direction
            guard.walls.add(wall_pos)
            if find_loop(guard):
                candidates.append(wall_pos)
            guard.walls.remove(wall_pos)
            guard.location, guard.direction = loc, dir_
        positions.add(guard.location)
        guard.move()
    
    print(len(set(candidates)))
    print(candidates)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
