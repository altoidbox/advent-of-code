#!/usr/bin/env python3

import argparse
import argparse
from pathlib import Path
import sys


# Add the common directory to the path
SCRIPT_DIR = Path(__file__).absolute().parent
sys.path.append(str(SCRIPT_DIR.parent.parent))


from common.grid import Grid
from common.point import Point


def readlines_stripped(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.rstrip('\r\n')
            data.append(line)
    return data


def load(path):
    data = []
    for line in readlines_stripped(path):
        x, y = [int(x) for x in line.split(',')]
        data.append(Point(x, y))
    return data


def square_size(p1, p2):
    diff = p2 - p1
    diff.x = abs(diff.x)
    diff.y = abs(diff.y)
    return (diff.x + 1) * (diff.y + 1)


def part1(path):
    red_tiles = load(path)
    max_area = 0
    for i1 in range(len(red_tiles)):
        for i2 in range(i1 + 1, len(red_tiles)):
            area = square_size(red_tiles[i1], red_tiles[i2])
            if area > max_area:
                max_area = area
    print(max_area)


def part2(path):
    red_tiles = load(path)
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
