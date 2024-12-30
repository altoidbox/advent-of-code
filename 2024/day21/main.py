#!/usr/bin/env python3

import argparse
from itertools import permutations
from functools import total_ordering
import math


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
    
    @property
    def tuple(self):
        return self.x, self.y

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


DIRS = {
    '^': Point(0, -1),
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0),
}
NUMPAD = {
    '7': Point(0, 0), '8': Point(1, 0), '9': Point(2, 0),
    '4': Point(0, 1), '5': Point(1, 1), '6': Point(2, 1),
    '1': Point(0, 2), '2': Point(1, 2), '3': Point(2, 2),
    ' ': Point(0, 3), '0': Point(1, 3), 'A': Point(2, 3),
}
NUMPAD.update({ v: k for k, v in NUMPAD.items() })
DIRPAD = {
    ' ': Point(0, 0), '^': Point(1, 0), 'A': Point(2, 0),
    '<': Point(0, 1), 'v': Point(1, 1), '>': Point(2, 1),
}
DIRPAD.update({ v: k for k, v in DIRPAD.items() })


PATH_BEST = {}
PATH_ALL = {}


def validate_path(path, start, keypad):
    pos = keypad[start]
    for dir_ in path:
        pos += DIRS[dir_]
        if keypad[pos] == ' ':
            return False
    return True


def navigate_pad_all(start, end, keypad) -> set[str]:
    if (start, end) in PATH_ALL:
        return PATH_ALL[(start, end)]
    moves = ''
    pos = keypad[start]
    new_pos = keypad[end]
    offset = new_pos - pos
    
    if offset.y < 0:
        upways = '^' * abs(offset.y)
    else:
        upways = 'v' * offset.y
    if offset.x >= 0:
        sideways = '>' * offset.x
    else:
        sideways = '<' * abs(offset.x)
    #all = set(''.join(move) + 'A' for move in permutations(moves, len(moves)) if validate_path(move, start, keypad))
    all = set(move + 'A' for move in [upways + sideways, sideways + upways] if validate_path(move, start, keypad))
    PATH_ALL[(start, end)] = all
    return all


def find_best_dirpad_path(path, best_dict):
    if path in best_dict:
        return best_dict[path]
    ways = set([''])
    cur = 'A'
    for c in path:
        new_ways = set()
        for next_way in navigate_pad_all(cur, c, DIRPAD):
            for way in ways:
                new_ways.add(way + next_way)
        ways = new_ways
        cur = c
    best_cost = math.inf
    best = set()
    for way in ways:
        cost = len(way)
        if cost < best_cost:
            best_cost = cost
            best = {way}
        elif cost == best_cost:
            best.add(way)
    best_dict[path] = best
    return best


def find_best_presses(start, end, depth):
    if (start, end) in PATH_BEST:
        return PATH_BEST[(start, end)]
    options = navigate_pad_all(start, end, NUMPAD)
    cur_best = {0: {None: options}}
    best_cost = 0
    for _ in range(depth):
        best_paths = {}
        best_moves = {}
        for path, options in cur_best[best_cost].items():
            for option in options:
                #print(path)
                more_options = find_best_dirpad_path(option, best_moves)
                first = next(iter(more_options))
                best_paths.setdefault(len(first), {})[option] = more_options
        best_cost = min(best_paths.keys())
        cur_best = best_paths
    
    first_path = next(iter(cur_best[best_cost]))
    first_solution = next(iter(cur_best[best_cost][first_path]))
    PATH_BEST[(start, end)] = first_solution
    #print(PATH_BEST[(start, end)])
    return PATH_BEST[(start, end)]


def best_cost_r(path, depth):
    if depth == 0:
        return len(path)
    if (path, depth) in PATH_BEST:
        return PATH_BEST[(path, depth)]
    options = find_best_dirpad_path(path, {})
    best_cost = math.inf
    best = None
    for option in options:
        cost = 0
        for seq in option.split('A')[:-1]:
            cost += best_cost_r(seq + 'A', depth - 1)
        if cost < best_cost:
            best_cost = cost
            best = option
    PATH_BEST[(path, depth)] = best_cost
    return best_cost


def part1(path):
    data = load(path)
    total = 0
    for combo in data:
        best = ''
        cur = 'A'
        for c in combo:
            best += find_best_presses(cur, c, 2)
            cur = c
        cval = int(combo[:3], 10)
        print(f'{combo}: {best} = {len(best)} * {cval}')
        total += len(best) * cval
    print(total)


def part2(path):
    PATH_BEST.clear()
    data = load(path)
    total = 0
    for combo in data:
        cur = 'A'
        cost = 0
        for c in combo:
            best_cost = math.inf
            options = navigate_pad_all(cur, c, NUMPAD)
            for opt in options:
                opt_cost = best_cost_r(opt, 25)
                if opt_cost < best_cost:
                    best_cost = opt_cost
            cost += best_cost
            cur = c
        cval = int(combo[:3], 10)
        print(f'{combo}: cost = {cost} * {cval}')
        total += cost * cval
    print(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()


# v<<A >>^A vA ^A v<<A >>^A A  v<A <A >>^A   A vA A <^A >A v<A >^A A <A >A  v<A <A >>^A A A vA <^A >A
#    <    A  >  A    <    A A    V  <    A   A  > >   ^  A   v   A A  ^  A    v  <    A A A  >   ^  A
#         ^     A         ^ ^            <   <           A       > >     A            v v v         A
#               3                                        7               9                          A

# <v<A >>^A vA ^A  <vA   <A A >>^A  A   vA <^A >A A  vA ^A <vA >^A A <A >A <v<A >A  >^A A A vA <^A >A
#    <    A  >  A    v    < <    A  A    >   ^  A A   >  A   v   A A  ^  A    <  v    A A A  >   ^  A
#         ^     A                <  <           ^ ^      A       > >     A            v v v         A
#               3                                        7               9                          A
