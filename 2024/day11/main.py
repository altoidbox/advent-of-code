#!/usr/bin/env python3

import argparse
from collections import defaultdict


def load(path):
    with open(path, "r") as f:
        data = [int(x) for x in f.read().strip().split()]
    return data


def blink(value):
    if value == 0:
        return [1]
    rep = str(value)
    if len(rep) & 1 == 0:
        half = len(rep) // 2
        v1 = int(rep[:half])
        v2 = int(rep[half:])
        return [v1, v2]
    value *= 2024
    return [value]


def part1(path):
    data = load(path)
    for _ in range(25):
        newlist = []
        for v in data:
            newlist.extend(blink(v))
        data = newlist
    print(len(data))


cache = {}


def solve(val, count):
    if count == 0:
        return 1
    key = (val, count)
    res = cache.get(key)
    if res is not None:
        return res
    res = 0
    for newval in blink(val):
        res += solve(newval, count - 1)
    cache[key] = res
    return res


def part2(path):
    data = load(path)
    res = 0
    for val in data:
        res += solve(val, 75)
    print(res)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
