#!/usr/bin/env python3

import argparse
import math
import heapq
from functools import total_ordering
from collections import defaultdict


def load(path):
    with open(path, "r") as f:
        data = [Point(*line.strip().split(',')) for line in f]
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


class Grid(dict):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    def copy(self):
        new_grid = Grid(self.width, self.height)
        for p, v in self.items():
            new_grid[p] = v
        return new_grid

    def __contains__(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def __getitem__(self, point):
        if point not in self:
            raise IndexError(f'Out of bounds: {point}')
        
        return super().get(point, '.')

    def __setitem__(self, point, value):
        if point not in self:
            raise IndexError(f'Out of bounds: {point}')
        return super().__setitem__(point, value)

    def __iter__(self):
        for y in range(0, self.width):
            for x in range(0, self.height):
                yield Point(x, y)
    
    def items(self):
        for p in self:
            yield p, self[p]

    def __str__(self):
        lines = []
        for y in range(0, self.width):
            line = ""
            for x in range(0, self.height):
                line += str(self.get(Point(x, y), '.'))
            lines.append(line)
        return "\n".join(lines)


DIRS = {
    '^': Point(0, -1),
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0),
}


class Maze(object):
    def __init__(self, grid):
        self.grid = grid
        self.start = Point(0, 0)
        self.end = Point(grid.width - 1, grid.height - 1)
        self.best_paths = {}

    def navigate(self):
        moves = [(0, self.start)]
        self.best_paths[self.start] = (0, None)
        while moves:
            cur_cost, cur = heapq.heappop(moves)
            for dir_ in '^>v<':
                child = cur + DIRS[dir_]
                if child not in self.grid:
                    # Out of bounds
                    continue
                if self.grid[child] == '#':
                    # No path can go from here to the end
                    continue
                child_cost = cur_cost + 1
                #cost, parent = self.best_paths.get(child, [(math.inf, None)])[0]
                best_cost, parent = self.best_paths.get(child, (math.inf, None))
                #if cost < child_cost or (cost == child_cost and parent == cur):
                if best_cost <= child_cost:
                    # We've already found a better path
                    continue
                #if cost == child_cost:
                #    self.best_paths[child].append((child_cost, cur))
                #else:
                #    self.best_paths[child] = [(child_cost, cur)]
                self.best_paths[child] = (child_cost, cur)
                #print(f'{cur}->{child} (beats {parent}->{child})')
                if child == self.end:
                    # Found the end
                    # print(f'{cur}->{child} (beats {parent}->{child})')
                    continue
                heapq.heappush(moves, (child_cost, child))
        best_cost, _ = self.best_paths.get(self.end, (None, None))
        return best_cost


def print_chosen_path(maze):
    grid = maze.grid.copy()
    cur = maze.end
    while cur is not None:
        grid[cur] = 'O'
        _, cur = maze.best_paths[cur]
    print(grid)


def part1(path):
    data = load(path)
    # handle test input different than real input
    if len(data) >= 1024:
        num_bytes = 1024
        grid = Grid(71, 71)
    else:
        num_bytes = 12
        grid = Grid(7, 7)

    for i in range(num_bytes):
        grid[data[i]] = '#'
    print(grid)
    maze = Maze(grid)
    maze.navigate()
    print_chosen_path(maze)
    best_cost, parent = maze.best_paths[maze.end]
    print(best_cost)


def part2(path):
    data = load(path)
    # handle test input different than real input
    if len(data) >= 1024:
        grid_size = 71
    else:
        grid_size = 7
    # Binary search for the number of bytes at which we can no longer find a path
    low = 0
    high = len(data)
    while low < high:
        mid = (low + high) // 2
        grid = Grid(grid_size, grid_size)
        for i in range(mid):
            grid[data[i]] = '#'
        maze = Maze(grid)
        cost = maze.navigate()
        if cost is None:
            # Did not find a path, need fewer bytes
            high = mid
        else:
            # Found a path, need more bytes
            low = mid + 1

    if cost is not None:
        index = mid
    else:
        index = mid + 1
    print_chosen_path(maze)
    print(cost)
    print(data[index])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
