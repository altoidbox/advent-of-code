#!/usr/bin/env python3

import argparse
import math


def readlines_stripped(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data


def load(path):
    banks = []
    for bank in readlines_stripped(path):
        banks.append([int(x) for x in bank])
    return banks


def max_split(bank, stop_idx):
    mv = -math.inf
    mi = -1
    for i, x in enumerate(bank):
        if i == stop_idx:
            break
        if x > mv:
            mv = x
            mi = i
    return mi, mv


def max_in_range(bank, start=0, stop=math.inf):
    mv = -math.inf
    mi = -1
    if stop > len(bank):
        stop = len(bank)
    for i in range(start, stop):
        x = bank[i]
        if x > mv:
            mv = x
            mi = i
    return mi, mv


def part1(path):
    total = 0
    for bank in load(path):
        idx, d1 = max_split(bank, len(bank) - 1)
        d2 = max(bank[idx+1:])
        joltage = d1 * 10 + d2
        total += joltage
    print(total)


def part2(path):
    total = 0
    digits = 12
    for bank in load(path):
        joltage = 0
        cur_idx = 0
        for idx in range(digits):
            to_leave = digits - idx - 1
            cur_idx, d = max_in_range(bank, start=cur_idx, stop=len(bank) - to_leave)
            cur_idx += 1
            joltage = joltage * 10 + d
        #print(joltage)
        total += joltage
    print(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
