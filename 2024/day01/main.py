#!/usr/bin/env python3
import argparse


def iabs(val):
    if val < 0:
        return -val
    return val


def read_input(path):
    left = []
    right = []
    with open(path) as f:
        for line in f:
            l, r = line.split()
            left.append(int(l))
            right.append(int(r))
    return list(sorted(left)), list(sorted(right))


def part1(path):
    dist = 0
    l, r = read_input(path)
    for a, b in zip(l, r):
        dist += iabs(a - b)
    print(dist)


def part2(path):
    l, r = read_input(path)
    i = j = 0
    total = 0
    prev = -1
    for i in range(len(l)):
        cur = l[i]
        if prev != cur:
            times = 0
        while j < len(r):
            other = r[j]
            if other > cur:
                break
            elif other == cur:
                times += 1
            j += 1
        total += cur * times
        #print(f"{cur} * {times}")
        prev = cur
    print(total)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('path')
    args = p.parse_args()

    part1(args.path)
    part2(args.path)