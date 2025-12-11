#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
import time


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
    return Grid(readlines_stripped(path))


def get_start(grid):
    for p, i in grid.items():
        if i == 'S':
            return p


MOVE_OFFSET = Point(0, 1)
SPLIT_OFFSETS = [Point(-1, 0), Point(1, 0)]


def move_beams(grid: Grid, beams: set):
    # make a copy and clear the original set
    old_locations = set(beams)
    beams.clear()
    splits = 0
    for beam in old_locations:
        # print(beam, beam + MOVE_OFFSET)
        beam += MOVE_OFFSET
        if grid.get(beam) == '^':
            # split beam
            beams.update((beam + offs) for offs in SPLIT_OFFSETS)
            splits += 1
        else:
            beams.add(beam)
    return splits


def part1(path):
    grid = load(path)
    start = get_start(grid)
    beams = {start}
    splits = 0
    while True:
        cur_splits = move_beams(grid, beams)
        splits += cur_splits
        if next(iter(beams)) not in grid:
            break
        # for beam in beams:
        #     grid[beam] = '|'
        # print(grid)
        # print()
        #time.sleep(0.25)
    print(splits, len(beams))


TIMELINE_MAP = {}


def move_beams_dfs(grid: Grid, beam: Point):
    # if we've already visited this point, we know how many timelines there are
    if beam in TIMELINE_MAP:
        return TIMELINE_MAP[beam]
    loc = grid.get(beam)
    if loc is None:
        # made it to the end of the manifold, this is one timeline
        timelines = 1
    elif loc == '^':
        # splitting the beam. number of timelines is equal to sum of split children
        timelines = 0
        for offs in SPLIT_OFFSETS:
            timelines += move_beams_dfs(grid, beam + offs)
    else:
        # not splitting, so same number of timelines as next move
        timelines = move_beams_dfs(grid, beam + MOVE_OFFSET)
    # save the result so next time we visit we can just return the value
    TIMELINE_MAP[beam] = timelines
    return timelines


def part2(path):
    grid = load(path)
    start = get_start(grid)
    count = move_beams_dfs(grid, start)
    print(count)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
