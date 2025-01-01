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
    
    def __str__(self):
        output = ''
        output += f'Button A: X+{self.a.x}, Y+{self.a.y}\n'
        output += f'Button B: X+{self.b.x}, Y+{self.b.y}\n'
        output += f'Prize: X={self.prize.x}, Y={self.prize.y}\n\n'
        return output


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
            elif line:
                raise ValueError(f'Unknown line: {line}')

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

    @property
    def tuple(self):
        return self.x, self.y


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
        # print(f'a:{a}, b:{b}')
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
    b = v // d
    a = (puzzle.prize.x - b * puzzle.b.x) // puzzle.a.x
    is_valid = (puzzle.a.x * a + puzzle.b.x * b) == puzzle.prize.x and (puzzle.a.y * a + puzzle.b.y * b) == puzzle.prize.y

    if is_valid:            
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
    for i, p in enumerate(data):
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
