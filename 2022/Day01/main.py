#!/usr/bin/env python3
import argparse
import heapq

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def part1(args):
    elves = []
    value = 0
    with open(args.input, 'rb') as f:
        for line in f:
            line = line.strip()
            if not line:
                elves.append(value)
                value = 0
                continue
            line_value = int(line.strip())
            value += line_value
    if value:
        elves.append(value)
    print("\nFinal Result1: {}".format(max(elves)))
    return elves


def part2(args):
    elves = part1(args)
    print("\nFinal Result2: {}".format(sum(heapq.nlargest(3, elves))))



if not args.part2:
    part1(args)
else:
    part2(args)

