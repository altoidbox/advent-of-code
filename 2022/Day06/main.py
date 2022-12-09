#!/usr/bin/env python3
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()

def load(args):
    lines = []
    with open(args.input, 'r') as f:
        for line in f:
            lines.append(line)
    return lines


def add(d, c):
    d[c] = d.setdefault(c, 0) + 1


def rem(d, c):
    d[c] -= 1
    if d[c] == 0:
        del d[c]


def find_start(data, size):
    marker = {}
    for i in range(len(data)):
        if i >= size:
            rem(marker, data[i-size])
        add(marker, data[i])
        if len(marker) == size:
            return i + 1
    return -1


def part1(data):
    for line in data:
        print(find_start(line, 4))


def part2(data):
    for line in data:
        print(find_start(line, 14))


data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

