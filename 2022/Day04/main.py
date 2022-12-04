#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class Range(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @staticmethod
    def parse(rg_string):    
        start, end = rg_string.split('-')
        return Range(int(start), int(end))
    
    def __contains__(self, other):
        return other.start >= self.start and other.end <= self.end
    
    def overlaps(self, other):
        return other.end >= self.start and self.end >= other.start

    def __str__(self):
        return '{}-{}'.format(self.start, self.end)


def load(args):
    pairs = []
    with open(args.input, 'r') as f:
        for line in f:
            line = line.strip()
            left, right = line.split(',')

            pairs.append((Range.parse(left), Range.parse(right)))
    return pairs



def part1(pairs):
    total = 0
    for (l, r) in pairs:
        if l in r or r in l:
            print(l, r)
            total += 1
    print(total)


def part2(pairs):
    total = 0
    for (l, r) in pairs:
        if l.overlaps(r):
            print(l, r)
            total += 1
    print(total)


data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

