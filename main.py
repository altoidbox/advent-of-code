#!/usr/bin/env python3

import argparse
import argparse
from pathlib import Path
import sys


# Add the common directory to the path
SCRIPT_DIR = Path(__file__).absolute().parent
sys.path.append(str(SCRIPT_DIR.parent.parent))


def readlines_stripped(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.rstrip('\r\n')
            data.append(line)
    return data


def load(path):
    return readlines_stripped(path)


def part1(path):
    pass


def part2(path):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
