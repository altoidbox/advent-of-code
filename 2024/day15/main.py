#!/usr/bin/env python3

import argparse
from collections import defaultdict


def load(path):
    with open(path, "r") as f:
        grid = []
        directions = ''
        state = 0
        for line in (line.strip() for line in f):
            if state == 0 and line:
                grid.append(line)
            elif not line:
                state += 1
            else:
                directions += line

    return grid, directions


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
    def limits(a, b):
        miny, maxy = min(a.y, b.y), max(a.y, b.y) + 1
        minx, maxx = min(a.x, b.x), max(a.x, b.x) + 1
        return (minx, maxx), (miny, maxy)
    
    @staticmethod
    def range(a, b):
        (minx, maxx), (miny, maxy) = Point.limits(a, b)
        for y in range(miny, maxy):
            changed_row = True
            for x in range(minx, maxx):
                yield Point(x, y), changed_row
                changed_row = False

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


ways = {
    '^': Point(0, -1),
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0),
}


def follow(grid, start, direction):
    cur = start + direction
    while grid[cur] == 'O':
        cur += direction
    if grid[cur] == '#':
        return start
    if grid[cur] == '.':
        grid[cur] = 'O'
        grid[start] = '.'
        cur = start + direction
        grid[cur] = '@'
        return cur
    raise Exception('Unexpected value')


def part1(path):
    lines, directions = load(path)
    grid = Grid(lines)
    for p, v in grid.items():
        if v == '@':
            cur = p
            break
    print(grid)
    for d in directions:
        cur = follow(grid, cur, ways[d])
    print(grid)
    answer = 0
    for p, v in grid.items():
        if v == 'O':
            answer += 100 * p.y + p.x
    print(answer)


class Box(object):
    OFFSET = Point(1, 0)

    def __init__(self, p=None):
        self.p = p
    
    def __hash__(self):
        return hash(self.p)

    def points(self):
        return [self.p, self.p + self.OFFSET]

    def move(self, chr):
        self.p += ways[chr]
    
    def adjacent(self, direction):
        adj = self.p + direction
        return [adj, adj + self.OFFSET]

    def __str__(self):
        return f'Box({self.p})'
    
    def __repr__(self):
        return f'B({self.p})'


class BoxGrid(dict):
    def __delitem__(self, key):
        if isinstance(key, Box):
            for p in key.points():
                super().__delitem__(p)
        else:
            super().__delitem__(key)

    def __setitem__(self, key, value):
        if isinstance(value, Box):
            value.p = key
            for p in value.points():
                super().__setitem__(p, value)
            return value
        else:
            return super().__setitem__(key, value)


def print_grid(grid, end):
    out = ''
    for p, new_row in Point.range(Point(0, 0), end):
        c = grid.get(p, '.')
        if isinstance(c, Box):
            if c.p == p:
                c = '['
            else:
                c = ']'
        out += c
        if p.x == end.x:
            print(out)
            out = ''


def move_boxes(grid, start, boxes, direction):
    # print(f'Moving {boxes} {direction}')
    # delete everything we're moving
    del grid[start]
    for b in boxes:
        del grid[b]
    # Now move them to the new locations
    for b in boxes:
        grid[b.p + direction] = b
    cur = start + direction
    grid[cur] = '@'
    return cur


def follow_side(grid, start, direction):
    cur = start + direction
    boxes = []
    while True:
        val = grid.get(cur)
        if not isinstance(val, Box):
            break
        boxes.append(val)
        cur += direction * 2
    if val == '#':
        return start
    if val is not None:
        raise Exception('Unexpected value')
    return move_boxes(grid, start, boxes, direction)


def follow_wide(grid, boxes, direction, all=None):
    if all is None:
        all = set()
    all.update(boxes)
    if not boxes:
        return all
    new_boxes = set()
    for b in boxes:
        for p in b.adjacent(direction):
            val = grid.get(p)
            # hit a wall
            if val == '#':
                return None
            if val is not None:
                new_boxes.add(val)
    return follow_wide(grid, new_boxes, direction, all)


def follow2(grid, start, chr):
    direction = ways[chr]
    if chr in '<>':
        return follow_side(grid, start, direction)
    cur = start + direction
    val = grid.get(cur)
    if val is None:
        boxes = []
    elif isinstance(val, Box):
        boxes = follow_wide(grid, {val}, direction)
    elif val == '#':
        boxes = None
    if boxes is None:
        return start
    return move_boxes(grid, start, boxes, direction)


def part2(path):
    lines, directions = load(path)
    grid = BoxGrid()
    cur = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                grid[Point(x * 2, y)] = '#'
                grid[Point(x * 2 + 1, y)] = '#'
            elif c == 'O':
                grid[Point(x * 2, y)] = Box()
            elif c == '@':
                cur = Point(x * 2, y)
                grid[cur] = '@'
    end = Point(x*2 + 1, y)
    print_grid(grid, end)
    for d in directions:
        cur = follow2(grid, cur, d)
    print_grid(grid, end)
    answer = 0
    boxes = {v for v in grid.values() if isinstance(v, Box)}
    for b in boxes:
        answer += 100 * b.p.y + b.p.x
    print(answer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
