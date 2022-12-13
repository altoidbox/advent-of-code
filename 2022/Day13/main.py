#!/usr/bin/env python3
import argparse
import re
from functools import cmp_to_key

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def load(path):
    pairs = [[]]
    with open(args.input, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if len(pairs[-1]) == 2:
                pairs.append([])
            pairs[-1].append(eval(line))
    return pairs


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    if isinstance(left, int):
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])
    # list compare
    for lchild, rchild in zip(left, right):
        res = compare(lchild, rchild)
        if res != 0:
            return res
    # child elements were identical
    return len(left) - len(right)


def part1(data):
    total = 0
    for i, (left, right) in enumerate(data):
        #print(compare(left, right), left, right)
        if compare(left, right) <= 0:
            total += i + 1
    print(total)


def part2(data):
    val = 1
    div1 = [[2]]
    div2 = [[6]]
    packs = [ div1, div2 ]
    for pair in data:
        packs.extend(pair)
    packs.sort(key=cmp_to_key(compare))
    for i, item in enumerate(packs):
        if item is div1 or item is div2:
            val *= (i + 1)
    print(val)


data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

