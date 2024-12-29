#!/usr/bin/env python3

import argparse
import math
import heapq
from functools import total_ordering
from collections import defaultdict


def load(path):
    with open(path, "r") as f:
        data = [line.strip() for line in f]
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

    def index(self, value, start=None, stop=None) -> Point:
        """
        Find the first occurrence of value in the grid.
        
        Args:
        value: the value to search for
        start: Point, the starting point of the search. Defaults to (0,0)
        stop: Point, the stopping point of the search. Defaults to (width-1, height-1)
        
        Returns:
        Point, the position of the first occurrence of value
        
        Raises:
        ValueError, if value is not in grid
        """
        if stop is None:
            stop = Point(self.width - 1, self.height - 1)
        if stop.x >= self.width:
            stop.x = self.width - 1
        if stop.y >= self.height:
            stop.y = self.height - 1
        if start is None:
            x, y = 0, 0
        else:
            x, y = start.x,start.y
        while y <= stop.y:
            p = Point(x, y)
            if self[p] == value:
                return p
            x += 1
            if x >= self.width:
                x = 0
                y += 1
            if y == stop.y and x > stop.x:
                break
        raise ValueError(f'{value} is not in grid')

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


DIRS = {
    '^': Point(0, -1),
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0),
}
RDIRS = {v: k for k, v in DIRS.items()}
OPPOSITE = {
    '^': 'v',
    '>': '<',
    'v': '^',
    '<': '>',
}


class Maze(object):
    def __init__(self, grid):
        self.grid = grid
        self.start = grid.index('S')
        self.end = grid.index('E')
        self.best_paths = {}
    
    def navigate(self):
        """
        We are going to find the shortest path from the end to the start
        since the puzzle input says there is exactly one path.
        We want to be able to easily calculate the distance from any given
        point to the end quickly.
        """
        moves = [(0, self.end)]
        self.best_paths[self.end] = (0, None)
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
                if child == self.start:
                    # Found the end
                    # print(f'{cur}->{child} (beats {parent}->{child})')
                    continue
                heapq.heappush(moves, (child_cost, child))
        best_cost, _ = self.best_paths.get(self.end, (None, None))
        return best_cost


def print_chosen_path(maze):
    grid = maze.grid.copy()
    _, cur = maze.best_paths[maze.start]
    while cur is not maze.end:
        grid[cur] = 'O'
        _, cur = maze.best_paths[cur]
    print(grid)


SKIPS = []
for dir1 in '^>v<':
    for dir2 in '^>v<':
        SKIPS.append(DIRS[dir1] + DIRS[dir2])


def find_cheats(maze):
    found = defaultdict(list)
    next_point = maze.start
    while next_point is not maze.end:
        cur_point = next_point
        cur_cost, next_point = maze.best_paths[cur_point]
        for cheat in SKIPS:
            cheat_point = cur_point + cheat
            if cheat_point not in maze.best_paths:
                continue
            cheat_cost, _ = maze.best_paths[cheat_point]
            cheat_cost += 2
            cheat_savings = cur_cost - cheat_cost
            if cheat_savings > 0:
                found[cheat_savings].append((cur_point, cheat_point))
    return found


def part1(path):
    data = load(path)
    grid = Grid(data)
    print(grid)
    maze = Maze(grid)
    maze.navigate()
    found = find_cheats(maze)
    if 0:
        for savings, points in sorted(found.items()):
            print(f'There are {len(points)} cheats that save {savings} picoseconds.')
            print(f'\t{points}')
    over_100 = 0
    for savings, points in sorted(found.items()):
        if savings >= 100:
            over_100 += len(points)
    print(over_100)


def all_within20(center, dist=20):
    N = Point(0, -1)
    E = Point(1, 0)
    S = Point(0, 1)
    W = Point(-1, 0)
    dirs = [(N, E), (E, S), (S, W), (W, N)]
    groups = [[center], [center], [center], [center]]
    all = set()
    for i in range(dist):
        for j, (group, moves) in enumerate(zip(groups, dirs)):
            new_group = set()
            for p in group:
                for move in moves:
                    new_group.add(p + move)
            groups[j] = new_group
            all.update(new_group)
    sides = {
        '^': [p - center for p in groups[0].union(groups[3])],
        '>': [p - center for p in groups[1].union(groups[0])],
        'v': [p - center for p in groups[2].union(groups[1])],
        '<': [p - center for p in groups[3].union(groups[2])],
    }
    return all, sides


def find_cheats20(maze):
    found = defaultdict(set)
    next_point = maze.start
    square, sides = all_within20(maze.start)
    cheat_points = set()
    for p in square:
        if p in maze.best_paths:
            cheat_points.add(p)
    while next_point is not maze.end:
        cur_point = next_point
        cur_cost, next_point = maze.best_paths[cur_point]
        for cheat_point in cheat_points:
            cheat_cost, _ = maze.best_paths[cheat_point]
            cheat_cost += cur_point.dist(cheat_point)
            cheat_savings = cur_cost - cheat_cost
            if cheat_savings > 0:
                found[cheat_savings].add((cur_point, cheat_point))
        
        #saved = {}
        #for p in square:
        #    if p in maze.grid:
        #        saved[p] = maze.grid[p]
        #        maze.grid[p] = '@'
        #saved[cur_point] = maze.grid[cur_point]
        #maze.grid[cur_point] = 'C'
        #print(maze.grid)
        #for p, val in saved.items():
        #    maze.grid[p] = saved[p]
        #input()

        # next_point = cur_point + dir_
        offs = next_point - cur_point
        dir_to = RDIRS[offs]
        dir_from = OPPOSITE[dir_to]
        #print(f'Going {dir_to} from {cur_point} to {next_point}')
        # Update square
        for edge_offset in sides[dir_to]:
            point = next_point + edge_offset
            square.add(point)
            if point in maze.best_paths:
                cheat_points.add(point)
        for edge_offset in sides[dir_from]:
            point = cur_point + edge_offset
            square.discard(point)
            cheat_points.discard(point)
            point += offs
    return found


def part2(path):
    data = load(path)
    grid = Grid(data)
    maze = Maze(grid)
    maze.navigate()
    found = find_cheats20(maze)
    if 0:
        for savings, points in sorted(found.items()):
            print(f'There are {len(points)} cheats that save {savings} picoseconds.')
            print(f'\t{points}')
    over_100 = 0
    for savings, points in sorted(found.items()):
        if savings >= 100:
            over_100 += len(points)
    print(over_100)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
