#!/usr/bin/env python3

import argparse
from functools import cached_property, cmp_to_key
from collections import defaultdict
import re
import math


class Puzzle(object):
    __slots__ = ['a', 'b', 'prize']
    def __repr__(self):
        return ', '.join(f'{k}: {getattr(self, k)}' for k in self.__slots__)


def load(path):
    data = []
    with open(path, "r") as f:
        cur = Puzzle()
        for line in (l.strip() for l in f):
            # Button A: X+94, Y+34
            # Button B: X+22, Y+67
            # Prize: X=8400, Y=5400
            m = re.match(r'Button (A|B): X\+(\d+), Y\+(\d+)', line)
            if m:
                setattr(cur, m.group(1).lower(), Point(int(m.group(2)), int(m.group(3))))
                continue
            m = re.match(r'Prize: X=(\d+), Y=(\d+)', line)
            if m:
                cur.prize = Point(int(m.group(1)), int(m.group(2)))
                data.append(cur)
                cur = Puzzle()

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

    def __cmp__(self, other):
        v = self.y - other.y
        if v == 0:
            return self.x - other.x
        return v

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

    @staticmethod
    def yrange(a, b):
        (minx, maxx), (miny, maxy) = Point.limits(a, b)
        for x in range(minx, maxx):
            changed_col = True
            for y in range(miny, maxy):
                yield Point(x, y), changed_col
                changed_col = False
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


def minmax(it, key=lambda x: x):
    min_ = max_ = None
    for item in it:
        val = key(item)
        if min_ is None or val < min_:
            min_ = val
        if max_ is None or val > max_:
            max_ = val
    return min_, max_


N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)
CARDINAL = [N, E, S, W]

# ax + by = c
# ai + bj = k
# 94a + 22b = 8400
# 34a + 67b = 5400
# 72x, 33y
# maxb = min( P(x) / B(x), P(y) / B(y) )

def solve(puzzle):
    # minimize number of times A is needed
    # a(A(x)) + b(B(x)) = P(x)
    # a = (P(x) - b(B(x))) / A(x)
    # a(A(y)) + b(B(y)) = P(y)
    # ( (P(x) - bB(x)) / A(x) )A(y) + bB(y) = P(y)
    # ( (P(x)A(y) - bB(x)A(y)) / A(x) ) + bB(y) = P(y)
    # (P(x)A(y) - bB(x)A(y)) / A(x) = P(y) - bB(y)
    # P(x)A(y) - bB(x)A(y) = P(y)A(x) - bB(y)A(x)
    # bB(y)A(x) - bB(x)A(y) = P(y)A(x) - P(x)A(y)
    # b(B(y)A(x) - B(x)A(y)) = P(y)A(x) - P(x)A(y)
    # b = ( P(y)A(x) - P(x)A(y) ) / ( B(y)A(x) - B(x)A(y) )
    v = puzzle.prize.y * puzzle.a.x - puzzle.prize.x * puzzle.a.y
    d = puzzle.b.y * puzzle.a.x - puzzle.b.x * puzzle.a.y
    # print(f'{v} / {d} == {v // d}')
    if v % d == 0:
        b = v // d
        a = (puzzle.prize.x - b * puzzle.b.x) // puzzle.a.x
        #print(p)
        #print(f'a:{a}, b:{b}')
        return a * 3 + b
    # print('None')
    return 0


def solve2(puzzle):
    # minimize number of times A is needed
    # aA(x) + bB(x) = P(x)
    # a = (P(x) - bB(x)) / A(x)
    # b = (P(x) - aA(x)) / B(x)
    # aA(y) + bB(y) = P(y)
    # a = (P(y) - bB(y)) / A(y)
    # b = (P(y) - aA(y)) / B(y)

    # A(y) = k * A(x)
    # B(y) = k * B(x)
    # P(y) = k * P(x)

    v = puzzle.prize.y * puzzle.a.x - puzzle.prize.x * puzzle.a.y
    d = puzzle.b.y * puzzle.a.x - puzzle.b.x * puzzle.a.y

    ka = math.lcm(puzzle.a.y, puzzle.b.y) / puzzle.b.y
    kb = math.lcm(puzzle.a.x, puzzle.b.x) / puzzle.b.x
    kc = puzzle.prize.y / puzzle.prize.x
    if ka == kb:
        print(puzzle)
        print(f'Common multiple: {ka}, {kb}, {kc}')

    # print(f'{v} / {d} == {v // d}')
    if v % d == 0:
        b = v // d
        a = (puzzle.prize.x - b * puzzle.b.x) // puzzle.a.x
            
        return a * 3 + b
    # print('None')
    return 0


def part1(path):
    data = load(path)
    total = 0
    for p in data:
        total += solve(p)
    print(total)


def part2(path):
    data = load(path)
    total = 0
    for p in data:
        p.prize.x += 10000000000000
        p.prize.y += 10000000000000
        total += solve2(p)
    print(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
