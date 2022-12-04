#!/usr/bin/env python3
import argparse
import heapq

parser = argparse.ArgumentParser()
parser.add_argument("input", default='input.txt')
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def load(args):
    sacks = []
    with open(args.input, 'r') as f:
        for line in f:
            line = line.strip()
            size = len(line) // 2
            sacks.append((line[:size], line[size:]))
    return sacks


def priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1
    return ord(item) - ord('A') + 27


def part1(sacks):
    total = 0
    for (l, r) in sacks:
        ls = set(l)
        rs = set(r)
        for item in l:
            if item in r:
                break
        else:
            print("fail")
        val = priority(item)
        total += val
        print(item, val, total)


def part2(sacks):
    total = 0
    group = None
    for i, (l, r) in enumerate(sacks):
        cur = set(l + r)
        if (i % 3) == 0:
            group = set(cur)
        group.intersection_update(cur)
        if (i%3) == 2:
            badge = group.pop()
            total += priority(badge)
            print(badge, total)


data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

