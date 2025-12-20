#!/usr/bin/env python3

import argparse
import argparse
from pathlib import Path
import sys
from itertools import chain


# Add the common directory to the path
SCRIPT_DIR = Path(__file__).absolute().parent
sys.path.append(str(SCRIPT_DIR.parent.parent))

import common
from common.debug import dprint
#common.debug.DEBUG = True


def readlines_stripped(path):
    with open(path, "r") as f:
        for line in f:
            line = line.rstrip('\r\n')
            yield line


def load(path):
    output_map = {}
    for line in readlines_stripped(path):
        source, outputs = line.split(':')
        outputs = outputs.strip().split(' ')
        output_map[source] = outputs
    return output_map


SOLUTIONS = {}
def _dfs(map, start: str, goal: str, parents: dict):
    if start in SOLUTIONS[goal]:
        return SOLUTIONS[goal][start]
    if start == goal:
        return 1
    if start in parents:
        # found a circular path, ignore it
        print(f'circular path: {".".join(parents.keys())}')
        return 0
    solutions = 0
    parents[start] = None
    for output in map.get(start, []):
        # originally this would keep track of possible solutions
        # but there were too many in part two, so now we just count
        # how many there are.
        solutions += _dfs(map, output, goal, parents)
    parents.popitem()
    SOLUTIONS[goal][start] = solutions
    return solutions


def dfs(map, start: str, goal='out'):
    if goal not in SOLUTIONS:
        SOLUTIONS[goal] = {}
    return _dfs(map, start, goal, {})


def part1(path):
    map = load(path)
    paths = dfs(map, 'you')
    print(paths)


def part2(path):
    map = load(path)
    # Assuming there are no loops, only one of these two routes will have a non-zero answer

    print('svr -> fft -> dac -> out')
    svr_fft = dfs(map, 'svr', 'fft')
    fft_dac = dfs(map, 'fft', 'dac')
    dac_out = dfs(map, 'dac', 'out')
    print(svr_fft * fft_dac * dac_out)

    print('svr -> dac -> fft -> out')
    svr_dac = dfs(map, 'svr', 'dac')
    dac_fft = dfs(map, 'dac', 'fft')
    fft_out = dfs(map, 'fft', 'out')
    print(svr_dac * dac_fft * fft_out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
