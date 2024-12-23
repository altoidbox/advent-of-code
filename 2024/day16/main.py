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

@total_ordering
class DirPoint(object):
    DIRS = {
        '^': Point(0, -1),
        '>': Point(1, 0),
        'v': Point(0, 1),
        '<': Point(-1, 0),
    }
    OPPOSITE = {
        '^': 'v',
        '>': '<',
        'v': '^',
        '<': '>',
    }
    TURN_COSTS = {
        '^': {'^': 0, '>': 1000, 'v': 2000, '<': 1000},
        '>': {'^': 1000, '>': 0, 'v': 1000, '<': 2000},
        'v': {'^': 2000, '>': 1000, 'v': 0, '<': 1000},
        '<': {'^': 1000, '>': 2000, 'v': 1000, '<': 0},
    }
    def __init__(self, point, direction, cost=0):
        self.point = point
        self.direction = direction
        self.cost = cost
    
    @property
    def tuple(self) -> tuple:
        return self.point.x, self.point.y, self.direction
    
    def __hash__(self):
        return hash(self.tuple)
    
    def __lt__(self, other):
        return self.tuple < other.tuple

    def __eq__(self, other):
        return self.tuple == other.tuple

    def __str__(self):
        return f'{self.point} {self.direction} {self.cost}'
    
    def __repr__(self):
        return f'DirPoint({self.point}, {self.direction}, {self.cost})'

    def next(self) -> 'DirPoint':
        """
        Move one step in the current direction.

        Returns:
            DirPoint: The point after moving one step.
        """
        return DirPoint(self.point + self.DIRS[self.direction], self.direction, self.cost + 1)
    
    def turn(self, direction) -> 'DirPoint':
        """
        Turn in the given direction.

        Args:
            direction: The direction to turn in (^, >, v, <).

        Returns:
            DirPoint: The point after turning in the given direction.
        """
        if direction == self.direction:
            return DirPoint(self.point + self.DIRS[self.direction], self.direction, self.cost + 1)
        if direction == self.OPPOSITE[self.direction]:
            return None
        return DirPoint(self.point, direction, self.cost + 1000)


class Path(object):
    def __init__(self, point):
        self.point = point
        self.cost = point.cost
    
    def add(self, point):
        self.points.append(point)
        self.cost += point.cost


class DfsState(object):
    def __init__(self, parent: 'DfsState', dirpoint):
        self.parent = parent
        self.dirpoint = dirpoint
        # We know we can from the opposite direction
        self.visited = '' # DirPoint.OPPOSITE[dirpoint.direction]
        self.paths = []
    
    def next_child(self):
        if not self.visited:
            self.visited += self.dirpoint.direction
            return self.dirpoint.next()
        for dir_ in '^>v<':
            if dir_ not in self.visited:
                self.visited += dir_
                return self.dirpoint.turn(dir_)
        return None
    
    def __repr__(self):
        return f'DfsState({self.dirpoint}, {self.visited})'


class Maze(object):
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.best_paths = defaultdict(list)
        self.visited = set()

    def navigate(self, start):
        moves = [(0, start)]
        self.best_paths[start].append((0, None))
        while moves:
            _cost, cur = heapq.heappop(moves)
            for dir_ in '^>v<':
                child = cur.turn(dir_)
                if child is None:
                    continue
                if self.grid[child.point] == '#':
                    # No path can go from here to the end
                    continue
                cost, parent = self.best_paths.get(child, [(math.inf, None)])[0]
                if cost < child.cost or (cost == child.cost and parent == cur):
                    # We've already found a better path
                    continue
                if cost == child.cost:
                    self.best_paths[child].append((child.cost, cur))
                else:
                    self.best_paths[child] = [(child.cost, cur)]
                #print(f'{cur}->{child} (beats {parent}->{child})')
                if child.point == self.end:
                    # Found the end
                    # print(f'{cur}->{child} (beats {parent}->{child})')
                    continue
                heapq.heappush(moves, (child.cost, child))

    def navigate_dfs(self, start):
        root = DfsState(None, start)
        moves = [DfsState(root, start)]
        self.visited.add(start.point)
        while moves:
            state = moves[-1]
            cur = state.next_child()
            if cur is None:
                # Need to evaluate child paths to determine best path from this point, and inform the parent
                if len(state.paths) == 0:
                    # No path can go from here to the end
                    self.best_paths[state.dirpoint] = None
                else:
                    # From all possible paths, choose the one with the lowest cost
                    best = min(state.paths, key=lambda p: p.cost)
                    # Save the location of the best path
                    self.best_paths[state.dirpoint] = best
                    # Add the best path to the parent
                    state.parent.paths.append(DirPoint(state.dirpoint.point, state.dirpoint.direction, best.cost + state.dirpoint.cost))
                moves.pop()
                self.visited.remove(state.dirpoint.point)
                continue
            if cur.point in self.visited:
                # We've already visited this point
                continue
            if cur in self.best_paths:
                # We already know the best path
                path = self.best_paths[cur]
                if path is not None:
                    state.paths.append(DirPoint(cur.point, cur.direction, path.cost + cur.cost))
                continue
            if cur.point == self.end:
                # Found the end
                state.paths.append(DirPoint(cur.point, cur.direction, cur.cost))
                continue
            if self.grid[cur.point] == '#':
                # No path can go from here to the end
                continue

            # done with all the easy cases, need to evaluate this node's children
            moves.append(DfsState(state, cur))
            self.visited.add(cur.point)
        return root.paths[0]
    
    def navigate_codium(self, start):
        stack = [start]
        while stack:
            cur = stack.pop()
            if cur.point in self.visited:
                continue
            if cur in self.best_paths:
                path = self.best_paths[cur]
                if path is not None:
                    stack.append(DirPoint(cur.point, cur.direction, path.cost + cur.cost))
                continue
            if cur.point == self.end:
                self.best_paths[cur] = DirPoint(cur.point, cur.direction, cur.cost)
                continue
            if self.grid[cur.point] == '#':
                self.best_paths[cur] = None
                continue

            self.visited.add(cur.point)
            stack.append(cur.next())
            for dir_ in 'v^<>':
                if dir_ == cur.direction:
                    continue
                stack.append(cur.turn(dir_))
            self.visited.remove(cur.point)

        best = self.best_paths.get(start)
        if best is None:
            return None
        return DirPoint(start.point, start.direction, best.cost + start.cost)
    
    def navigate_recursive(self, cur):
        if cur.point in self.visited:
            # We've already visited this point
            return None
        if cur in self.best_paths:
            # We already know the best path
            path = self.best_paths[cur]
            if path is None:
                return None
            return DirPoint(cur.point, cur.direction, path.cost + cur.cost)
        if cur.point == self.end:
            # Found the end
            return DirPoint(cur.point, cur.direction, cur.cost)
        if self.grid[cur.point] == '#':
            # No path can go from here to the end
            return None

        self.visited.add(cur.point)
        #print(f'Visiting {cur}')
        best = self.navigate(cur.next())
        for dir_ in '^>v<':
            if dir_ == cur.direction:
                continue
            path = self.navigate(cur.turn(dir_))
            if path is None:
                continue
            if best is None or path.cost < best.cost:
                best = path
        self.visited.remove(cur.point)
        self.best_paths[cur] = best
        if best is None:
            return None

        return DirPoint(cur.point, cur.direction, best.cost + cur.cost)


def print_chosen_path(maze):
    grid = maze.grid.copy()
    cur_dp = maze.best_paths[DirPoint(maze.start, '>')]
    while cur_dp.point != maze.end:
        #print(cur_dp)
        grid[cur_dp.point] = cur_dp.direction
        cur_dp = maze.best_paths[cur_dp]
    print(grid)


def print_all_paths(maze):
    grid = maze.grid.copy()
    for p, v in grid.items():
        if v == '#':
            continue
        for dir_ in 'v^<>':
            dp = DirPoint(p, dir_)
            if maze.best_paths.get(dp) is not None:
                grid[p] = maze.best_paths[dp].direction
    print(grid)


def part1(path):
    grid = Grid(load(path))
    start = grid.index('S')
    end = grid.index('E')
    print(grid)
    print(start)
    print(end)
    maze = Maze(grid, start, end)
    start_dp = DirPoint(start, '>')
    maze.navigate(start_dp)
    best = []
    for dir_ in '^>v<':
        dp = DirPoint(end, dir_)
        cost, p = maze.best_paths.get(dp, [(math.inf, None)])[0]
        if p is None:
            continue
        dp.cost = cost
        if len(best) == 0:
            best.append(dp)
        elif cost < best[0].cost:
            best = [dp]
        elif cost == best[0].cost:
            best.append(dp)
    print(best)

    #print('Chosen path:')
    #print_chosen_path(maze)
    #print('All paths:')
    #print_all_paths(maze)

    #print(maze.best_paths[start_dp])
    #print(path.points)
    #print(cost)


def follow(maze, paths):
    on_path = set()
    visited = set()
    while paths:
        cur = paths.pop()
        if cur in visited:
            continue
        visited.add(cur)
        on_path.add(cur.point)
        if cur.point == maze.start:
            continue
        parents = maze.best_paths[cur]
        if len(parents) > 1:
            print('Multiple parents:', parents)
        for cost, p in parents:
            paths.append(p)
    return on_path


def part2(path):
    grid = Grid(load(path))
    start = grid.index('S')
    end = grid.index('E')
    maze = Maze(grid, start, end)
    start_dp = DirPoint(start, '>')
    maze.navigate(start_dp)
    best = []
    for dir_ in '^>v<':
        dp = DirPoint(end, dir_)
        cost, p = maze.best_paths.get(dp, [(math.inf, None)])[0]
        if p is None:
            continue
        dp.cost = cost
        if len(best) == 0:
            best.append(dp)
        elif cost < best[0].cost:
            best = [dp]
        elif cost == best[0].cost:
            best.append(dp)
    #print(best)
    on_path = follow(maze, best)
    print(len(on_path))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
