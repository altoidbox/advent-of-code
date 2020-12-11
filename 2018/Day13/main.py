import argparse
import re
from collections import OrderedDict, deque
import heapq
import sys


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


DIR_MAP = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1)
}

LEFT_TURN_MAP = {
    '>': '^',
    '^': '<',
    '<': 'v',
    'v': '>'
}
STRAIGHT_MAP = {
    '>': '>',
    'v': 'v',
    '<': '<',
    '^': '^'
}
RIGHT_TURN_MAP = {
    '>': 'v',
    'v': '<',
    '<': '^',
    '^': '>'
}
INTERSECTION_MAP = {
    0: LEFT_TURN_MAP,
    1: STRAIGHT_MAP,
    2: RIGHT_TURN_MAP
}


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tuple(self):
        return self.x, self.y

    @property
    def sort_value(self):
        return self.y, self.x

    def __str__(self):
        return "<{}, {}>".format(self.x, self.y)

    def __repr__(self):
        return "<{}, {}>".format(self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Point):
            x, y = other.x, other.y
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            x, y = other
        else:
            raise ValueError()
        return Point(x + self.x, y + self.y)


BSLASH_MAP = {
    '^': '<',
    '<': '^',
    'v': '>',
    '>': 'v'
}

SLASH_MAP = {
    '^': '>',
    '>': '^',
    'v': '<',
    '<': 'v'
}

TURN_MAP = {
    '\\': BSLASH_MAP,
    '/': SLASH_MAP
}


class Collision(Exception):
    pass


class Cart(object):
    def __init__(self, x, y, d):
        self.point = Point(x, y)
        self.d = d
        self.turn_idx = 0

    def move(self, track):
        self.point += DIR_MAP[self.d]
        t = track[self.point.y][self.point.x]
        if t in ('-', '|'):
            return
        if t == '+':
            self.d = INTERSECTION_MAP[self.turn_idx][self.d]
            self.turn_idx = (self.turn_idx + 1) % 3
            return
        self.d = TURN_MAP[t][self.d]


class Puzzle(object):
    def __init__(self):
        self.args = None

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("input")
        parser.add_argument("--part2", action="store_true")
        self.args = parser.parse_args()
        if args.part2:
            self.part2()
        else:
            self.part1()

    def read_input(self):
        grid = []
        carts = []
        with open(args.input, "r") as f:
            for line in f:
                line = list(line)
                for i, t in enumerate(line):
                    if t in ('>', '<', '^', 'v'):
                        carts.append(Cart(i, len(grid), t))
                        if t in ('>', '<'):
                            line[i] = '-'
                        else:
                            line[i] = '|'
                grid.append(line)

        return grid, carts

    def move(self, grid, carts):
        moved = set()
        for cart in carts:
            cart.move(grid)
            p = cart.point.tuple
            if p in moved:
                raise Collision("Collision at {}".format(p))
            moved.add(p)
        carts.sort(key=lambda c: c.point.sort_value)

    def part1(self):
        grid, carts = self.read_input()
        i = 0
        try:
            while True:
                i += 1
                self.move(grid, carts)
        except Collision as e:
            print("{}: {}".format(i, e))

    def safe_move(self, grid, carts):
        for cart in list(sorted(carts.values(), key=lambda c: c.point.sort_value)):
            cart = carts.pop(cart.point.tuple, None)
            if not cart:
                continue
            cart.move(grid)
            collided_cart = carts.pop(cart.point.tuple, None)
            if collided_cart:
                continue
            carts[cart.point.tuple] = cart

    def part2(self):
        grid, carts = self.read_input()
        carts = {c.point.tuple: c for c in carts}
        i = 0
        while len(carts) > 1:
            i += 1
            self.safe_move(grid, carts)
        for cart in carts.values():
            print("{}".format(cart.point))


Puzzle().parse_args()
