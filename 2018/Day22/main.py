import argparse
from datetime import datetime
import re
from collections import deque
import heapq


def yc(point):
    return point[1]


def xc(point):
    return point[0]


def add_points(left, right):
    return left[0] + right[0], left[1] + right[1]


ADJACENTS = ((-1, 0), (0, -1), (0, 1), (1, 0))


def get_adjacents(grid, point, type_):
    values = []
    for offs in ADJACENTS:
        p = add_points(point, offs)
        if grid.get(p) == type_:
            values.append(p)
    return values


def find_first_move(moves, end_point):
    move = end_point
    depth, edge = moves[move]
    while depth > 1:
        # print("{}: {}".format(depth, move))
        move = edge
        depth, edge = moves[move]
    # print("{}: {}*".format(depth, move))
    return move


class Bounds(object):
    def __init__(self, points):
        self.minx = min(p[0] for p in points)
        self.maxx = max(p[0] for p in points)
        self.miny = min(p[1] for p in points)
        self.maxy = max(p[1] for p in points)

    def xrange(self):
        return range(self.minx, self.maxx + 1)

    def yrange(self):
        return range(self.miny, self.maxy + 1)

    @property
    def width(self):
        return self.maxx - self.minx + 1

    @property
    def height(self):
        return self.maxy - self.miny + 1


class BoundedGrid(object):
    def __init__(self, bounds):
        self.bounds = bounds
        self.grid = []
        for _ in range(bounds.maxx - bounds.minx + 1):
            self.grid.append([None] * (bounds.maxy - bounds.miny + 1))
        self.set_elements = 0

    def contains(self, point):
        return self.bounds.minx <= point.x <= self.bounds.maxx and self.bounds.miny <= point.y <= self.bounds.maxy

    def get(self, point):
        return self.grid[point.x - self.bounds.minx][point.y - self.bounds.miny]

    def set(self, point, item):
        self.grid[point.x - self.bounds.minx][point.y - self.bounds.miny] = item


VALID_TOOLS = {
    0: {'C', 'T'},
    1: {'C', 'N'},
    2: {'T', 'N'}
}


class Room:
    IMAGES = ['.', '=', '|']

    def __init__(self, index, depth):
        self.index = index
        self.erosion = (index + depth) % 20183
        self.type = self.erosion % 3

    @property
    def image(self):
        return Room.IMAGES[self.type]


def calc_move_cost(equipment, from_room, to_room):
    """:raises KeyError on failure"""
    # assume we have equipment for the current room
    if equipment in VALID_TOOLS[to_room.type]:
        return equipment, 1
    shared = VALID_TOOLS[from_room.type].intersection(VALID_TOOLS[to_room.type]).pop()
    return shared, 7 + 1


class MinHeapDict:
    def __init__(self):
        self.heap = []
        self.dict = {}

    def push(self, priority, key, value):
        old = self.dict.get(key)
        if old is not None:
            if old[0] <= priority:
                return
            else:
                old[2] = None
        # print("edge {} {} -> {}".format(priority, key, value))
        qvalue = [priority, key, value]
        self.dict[key] = qvalue
        heapq.heappush(self.heap, qvalue)

    def pop(self):
        while True:
            result = heapq.heappop(self.heap)
            if result[2] is not None:
                self.dict.pop(result[1])
                return result


class Cave:
    def __init__(self, depth=4845, target=(6, 770), size=(106, 870)):
        self.depth = depth
        self.target = target
        self.bounds = Bounds([(0, 0), self.target, size])
        self.map = {}

    def generate(self):
        y = 0
        for x in self.bounds.xrange():
            self.map[(x, y)] = Room(x * 16807, self.depth)
        x = 0
        for y in self.bounds.yrange():
            self.map[(x, y)] = Room(y * 48271, self.depth)
        self.map[(0, 0)] = Room(0, self.depth)
        for y in range(1, self.bounds.maxy + 1):
            for x in range(1, self.bounds.maxx + 1):
                if x == xc(self.target) and y == yc(self.target):
                    self.map[self.target] = Room(0, self.depth)
                    continue
                index = self.map[(x-1, y)].erosion * self.map[(x, y-1)].erosion
                self.map[(x, y)] = Room(index, self.depth)

    def risk(self):
        risk = 0
        for y in self.bounds.yrange():
            for x in self.bounds.xrange():
                risk += self.map[(x, y)].type
        return risk

    def print(self):
        for y in self.bounds.yrange():
            print(''.join(self.map[(x, y)].image for x in self.bounds.xrange()))

    def shortest_paths(self):
        edges = MinHeapDict()
        edges.push(0, ((0, 0), 'T'), (None, 'T'))
        moves = {((0, 0), 'T'): (0, ((0, 0), 'T'))}
        while True:
            cost, (edge, edge_equipment), (parent, parent_equipment) = edges.pop()
            moves[(edge, edge_equipment)] = (cost, (parent, parent_equipment))
            # print(edge, cost, parent, edge_equipment)
            if edge == self.target:
                if edge_equipment is not 'T':
                    moves[(edge, 'T')] = (cost + 7, (edge, edge_equipment))
                print("Found path to {} in {} minutes".format(edge, moves[(edge, 'T')][0]))
                break
            for offset in ADJACENTS:
                move = add_points(edge, offset)
                if move not in self.map:
                    # if xc(move) > 0 and yc(move) > 0:
                    #     print("reached edge: {}".format(move))
                    continue
                try:
                    move_equipment, move_cost = calc_move_cost(edge_equipment, self.map[edge], self.map[move])
                except KeyError:
                    # illegal move
                    continue
                if (move, move_equipment) in moves:
                    # already have shortest path to this node
                    # if cost + move_cost < moves[move][0]:
                    #     print("Failed...")
                    continue
                # print("add {} {} -> {}".format(depth+1, edge, move))
                edges.push(cost + move_cost, (move, move_equipment), (edge, edge_equipment))
        return moves


def target_path(moves, target):
    cur = target
    path = []
    while cur[0] is not None:
        cost, parent = moves[cur]
        path.append((cost, cur))
        cur = parent
    return reversed(path)


def part1(args):
    #cave = Cave(depth=510, target=(10, 10))
    cave = Cave()
    cave.generate()
    cave.print()
    print(cave.risk())


def part2(args):
    # cave = Cave(depth=510, target=(10, 10), size=(20, 20))
    cave = Cave()
    cave.generate()
    # cave.print()
    moves = cave.shortest_paths()
    # for move in target_path(moves, (cave.target, 'T')):
    #     print(move)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--part2", action="store_true")

    args = parser.parse_args()

    if args.part2:
        part2(args)
    else:
        part1(args)
