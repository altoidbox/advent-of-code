import argparse
import re
from collections import OrderedDict, deque
import heapq
import sys


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


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

    def combine(self, recipies, a, b):
        c = recipies[a] + recipies[b]
        if c < 10:
            return c,
        return 1, c-10

    def part1(self):
        input = int(args.input)
        recipies = [3, 7]
        e1 = 0
        e2 = 1
        while len(recipies) < input + 10:
            recipies.extend(self.combine(recipies, e1, e2))
            e1 = (e1 + 1 + recipies[e1]) % len(recipies)
            e2 = (e2 + 1 + recipies[e2]) % len(recipies)
        print(''.join(str(i) for i in recipies[input:input+10]))

    def compare(self, search, lst):
        if len(lst) < len(search):
            return False
        for i in range(-len(search), 0):
            if search[i] != lst[i]:
                return False
        return True

    def find_it(self):
        recipies = [3, 7]
        e1 = 0
        e2 = 1
        input_ = list(map(int, args.input))
        while True:
            values = self.combine(recipies, e1, e2)
            for v in values:
                recipies.append(v)
                if self.compare(input_, recipies):
                    return len(recipies) - len(input_)
            e1 = (e1 + 1 + recipies[e1]) % len(recipies)
            e2 = (e2 + 1 + recipies[e2]) % len(recipies)

    def part2(self):
        print(self.find_it())


Puzzle().parse_args()
