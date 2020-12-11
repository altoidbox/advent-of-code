import argparse
import re
from collections import OrderedDict, deque
import heapq
import sys


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def rrange(end):
    return range(end-1, 0-1, -1)


def y(point):
    return point[0]


def x(point):
    return point[1]


def add_points(left, right):
    return left[0] + right[0], left[1] + right[1]


def make_point(y=y, x=x):
    return y, x


DIR_MAP = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

OPP_MAP = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}


class Room:
    def __init__(self, y, x):
        self.point = (y, x)
        self.doors = set()

    def neighbors(self):
        return (add_points(self.point, DIR_MAP[d]) for d in self.doors)


class Building:
    def __init__(self):
        self.rooms = {
            (0, 0): Room(0, 0)
        }
        self.bounds = Bounds([(0, 0)])

    def move(self, room, direction):
        room.doors.add(direction)
        new_point = add_points(room.point, DIR_MAP[direction])
        new_room = self.rooms.get(new_point)
        if new_room is None:
            new_room = Room(*new_point)
            self.rooms[new_point] = new_room
            self.bounds.add_point(new_point)
        new_room.doors.add(OPP_MAP[direction])
        return new_room

    def merge(self, start, other):
        if len(self.rooms) == 1:
            self.rooms = other.rooms
            self.bounds = other.bounds
            return
        offset = start.point
        for room in other.rooms.values():
            point = add_points(room.point, offset)
            my_room = self.rooms.get(point)
            if not my_room:
                my_room = Room(*point)
                self.rooms[point] = my_room
                self.bounds.add_point(point)
            my_room.doors.update(room.doors)

    def draw(self):
        h = self.bounds.height * 2 + 1
        w = self.bounds.width * 2 + 1
        prev = None
        cur = None
        next_ = [' '] * w
        for y in range(self.bounds.miny, self.bounds.maxy + 1):
            if prev is not None:
                print(''.join(prev))
                print(''.join(cur))
            prev = next_
            cur = [' '] * w
            next_ = [' '] * w
            dy = 2 * (y - self.bounds.miny + 1)
            for x in range(self.bounds.minx, self.bounds.maxx + 1):
                # Draw each room
                room = self.rooms.get((y, x), None)
                if room is None:
                    continue
                dx = 2 * (x - self.bounds.minx) + 1
                prev[dx - 1] = '#'
                prev[dx] = '-' if 'N' in room.doors else '#'
                prev[dx + 1] = '#'
                cur[dx - 1] = '|' if 'W' in room.doors else '#'
                cur[dx] = 'X' if x == 0 and y == 0 else '.'
                cur[dx + 1] = '|' if 'E' in room.doors else '#'
                next_[dx - 1] = '#'
                next_[dx] = '-' if 'S' in room.doors else '#'
                next_[dx + 1] = '#'
        print(''.join(prev))
        print(''.join(cur))
        print(''.join(next_))


class Bounds(object):
    def __init__(self, points):
        self.minx = min(p[1] for p in points)
        self.maxx = max(p[1] for p in points)
        self.miny = min(p[0] for p in points)
        self.maxy = max(p[0] for p in points)

    @property
    def height(self):
        return self.maxy - self.miny + 1

    @property
    def width(self):
        return self.maxx - self.minx + 1

    def add_point(self, point):
        if x(point) > self.maxx:
            self.maxx = x(point)
        elif x(point) < self.minx:
            self.minx = x(point)
        if y(point) > self.maxy:
            self.maxy = y(point)
        elif y(point) < self.miny:
            self.miny = y(point)

    def extend(self, point):
        if x(point) > 0:
            self.maxx += x(point)
        elif x(point) < 0:
            self.minx += x(point)
        if y(point) > 0:
            self.maxy += y(point)
        elif y(point) < 0:
            self.miny += y(point)


class BoundedGrid(object):
    def __init__(self, bounds, empty):
        self.bounds = bounds
        self.grid = []
        for _ in range(bounds.maxy - bounds.miny + 1):
            self.grid.append([empty] * (bounds.maxx - bounds.minx + 1))

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def contains(self, point):
        return self.bounds.minx <= x(point) <= self.bounds.maxx and self.bounds.miny <= y(point) <= self.bounds.maxy

    def get(self, point):
        try:
            return self.grid[point[0] - self.bounds.miny][point[1] - self.bounds.minx]
        except IndexError:
            return None

    def set(self, point, item):
        self.grid[point[0] - self.bounds.miny][point[1] - self.bounds.minx] = item


class TreeNode:
    def __init__(self):
        self.value = ''
        self.children = []
        self.solution = None


def make_tree(data):
    root = cur = TreeNode()
    stack = []
    for move in data:
        if move == '(':
            # print("push", i)
            decision_node = TreeNode()
            cur.children.append(decision_node)
            cur = TreeNode()
            decision_node.children.append(cur)
            stack.append((decision_node, []))
        elif move == '|':
            stack[-1][1].append(cur)
            cur = TreeNode()
            stack[-1][0].children.append(cur)
        elif move == ')':
            stack[-1][1].append(cur)
            # print("pop", i)
            decision_node, child_leaves = stack.pop()
            cur = TreeNode()
            for node in child_leaves:
                node.children.append(cur)
        elif move == '$':
            break
        elif move == '^':
            pass
        else:
            cur.value += move
    return root


def read_input(path):
    with open(path, "r") as f:
        for line in f:
            return line


def print_grid(grid):
    print('\n'.join(''.join(n.state for n in row) for row in grid))


def furthest_room(rooms):
    start = (0, 0)
    edges = deque()
    edges.append((0, start))
    moves = {start: (0, start)}
    while len(edges):
        depth, edge = edges.popleft()
        for move in rooms[edge].neighbors():
            if move in moves:
                continue
            # print("add {} {} -> {}".format(depth+1, edge, move))
            moves[move] = depth + 1, edge
            edges.append((depth + 1, move))
    # Found all shortest paths... Now figure out which one to pursue
    furthest = max(v[0] for v in moves.values())
    over_1000 = 0
    for value in moves.values():
        if value[0] >= 1000:
            over_1000 += 1
    return furthest, over_1000


def build_wtree(data):
    tree = make_tree(data)
    b = Building()
    room = b.rooms[(0, 0)]
    paths = deque()
    paths.append((room, tree))
    while len(paths):
        room, node = paths.popleft()
        for move in node.value:
            room = b.move(room, move)
        for child in node.children:
            paths.append((room, child))
    b.draw()
    print(furthest_room(b.rooms))


def build_wtree_dyn_node(root):
    if root.solution:
        return root.solution
    root.solution = Building()
    room = root.solution.rooms[(0, 0)]
    for move in root.value:
        room = root.solution.move(room, move)
    for child in root.children:
        root.solution.merge(room, build_wtree_dyn_node(child))
    return root.solution


def build_wtree_dyn(data):
    tree = make_tree(data)
    b = build_wtree_dyn_node(tree)
    b.draw()
    print(furthest_room(b.rooms))


def build(data):
    b = Building()
    room = b.rooms[(0, 0)]
    stack = []
    moves = deque()
    i = 0
    while True:
        move = data[i]
        if move == '(':
            # print("push", i)
            stack.append((room, []))
        elif move == '|':
            stack[-1][1].append(room)
            room = stack[-1][0]
        elif move == ')':
            # print("pop", i)
            _, ends = stack.pop()
            for r in ends:
                moves.append((r, i, list(stack)))
        elif move == '$':
            if len(moves) == 0:
                break
            else:
                room, i, stack = moves.popleft()
        elif move == '^':
            pass
        else:
            room = b.move(room, move)
        i += 1
    b.draw()
    print(furthest_room(b.rooms))


def part1(args):
    build_wtree_dyn(read_input(args.input))
    return
    data = [
        '^WNE$',
        '^ENWWW(NEEE|SSE(EE|N))$',
        '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$',
        '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$',
        '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
    ]
    for d in data:
        build_wtree_dyn(d)


def part2(args):
    build_wtree_dyn(read_input(args.input))
    return


if args.part2:
    part2(args)
else:
    part1(args)
