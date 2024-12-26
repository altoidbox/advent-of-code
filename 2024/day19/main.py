#!/usr/bin/env python3

import argparse
from functools import total_ordering
from collections import defaultdict


def load(path):
    with open(path, "r") as f:
        avail = [value.strip() for value in f.readline().split(',')]
        f.readline()
        patterns = [line.strip() for line in f]
    return avail, patterns


def can_craft(pattern, towels, possible):
    if len(pattern) == 0:
        return True
    if pattern in possible:
        return possible[pattern]
    for t in towels[pattern[0]]:
        if pattern.startswith(t):
            if can_craft(pattern[len(t):], towels, possible):
                possible[pattern] = True
                return True
    possible[pattern] = False
    return False


def part1(path):
    towels, patterns = load(path)
    towel_map = defaultdict(list)
    for t in towels:
        towel_map[t[0]].append(t)
    for t in towel_map:
        towel_map[t] = sorted(towel_map[t], key=lambda x: len(x), reverse=True)
    
    print(patterns)
    print(towel_map)

    count = 0
    possible = {}
    for p in patterns:
        if can_craft(p, towel_map, possible):
            count += 1
    print(count)


def ways_to_craft(pattern, towels, num_ways):
    if len(pattern) == 0:
        return 1
    if pattern in num_ways:
        return num_ways[pattern]
    count = 0
    for t in towels[pattern[0]]:
        if pattern.startswith(t):
            count += ways_to_craft(pattern[len(t):], towels, num_ways)
    num_ways[pattern] = count
    return count


def part2(path):
    towels, patterns = load(path)
    towel_map = defaultdict(list)
    for t in towels:
        towel_map[t[0]].append(t)
    for t in towel_map:
        towel_map[t] = sorted(towel_map[t], key=lambda x: len(x), reverse=True)
    
    count = 0
    num_ways = {}
    for p in patterns:
        count += ways_to_craft(p, towel_map, num_ways)
    print(count)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
