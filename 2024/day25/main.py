#!/usr/bin/env python3

import argparse
import math
import heapq
from functools import total_ordering
from collections import defaultdict


def load(path):
    data = [[]]
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                data.append([])
            else:
                data[-1].append(line)
    return data


def part1(path):
    data = load(path)
    keys = []
    locks = []
    for obj in data:
        max_height = len(obj)
        heights = [0] * len(obj[0])
        if obj[0][0] == '#':
            yrange = range(1, len(obj))
            locks.append(heights)
        else:
            yrange = range(len(obj) - 2, -1, -1)
            keys.append(heights)
        for x in range(len(obj[0])):
            for y in yrange:
                if obj[y][x] == '#':
                    heights[x] += 1
                else:
                    break
    
    max_height -= 2
    #print(max_height)
    #print(locks)
    #print(keys)
    matches = 0
    for lock in locks:
        for key in keys:
            for i in range(len(lock)):
                if lock[i] + key[i] > max_height:
                    break
            else:
                #print("Match", lock, key)
                matches += 1
    print(matches)


def part2(path):
    data = load(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
