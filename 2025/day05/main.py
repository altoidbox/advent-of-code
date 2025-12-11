#!/usr/bin/env python3

import argparse


def readlines_stripped(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data


def load(path):
    ranges = []
    ids = []
    stage = 0
    for line in readlines_stripped(path):
        if not line:
            stage += 1
            continue
        if stage == 0:
            start, end = line.split('-')
            ranges.append(range(int(start), int(end)+1))
        elif stage == 1:
            ids.append(int(line))
    return ranges, ids


def part1(path):
    ranges, ids = load(path)
    fresh = 0
    for id_ in ids:
        if any(id_ in rg for rg in ranges):
            fresh += 1
    print(fresh)


class RangeMap:
    def __init__(self):
        self.ranges = []

    def rebuild(self):
        ranges = self.ranges
        self.ranges = []
        for rg in ranges:
            self.add(rg)

    def add(self, rg):
        for i, r in enumerate(self.ranges):
            # if they overlap at all, merge them
            if (rg.start <= r.stop and rg.stop >= r.start) or (rg.start < r.stop and rg.stop >= r.start):
                new_range = range(min(rg.start, r.start), max(rg.stop, r.stop))
            else:
                # does not overlap
                continue
            # replace with the merged range
            self.ranges[i] = new_range
            # rebuild to see if this new range overlaps with any existing range
            self.rebuild()
            return
        self.ranges.append(rg)


def part2(path):
    ranges, ids = load(path)
    rmap = RangeMap()
    for rg in ranges:
        rmap.add(rg)
    # print(rmap.ranges)
    total = 0
    for rg in rmap.ranges:
        total += rg.stop - rg.start
    print(total)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
