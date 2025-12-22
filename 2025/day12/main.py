#!/usr/bin/env python3

import argparse
import argparse
from pathlib import Path
from functools import cached_property
import sys


# Add the common directory to the path
SCRIPT_DIR = Path(__file__).absolute().parent
sys.path.append(str(SCRIPT_DIR.parent.parent))


from common.grid import Grid


class Present(Grid):
    def __init__(self, values, origin=None):
        super().__init__(values)
        if origin is None:
            origin = self
        self.origin = origin

    @cached_property
    def tuple(self):
        return tuple((tuple(row) for row in self.values))

    def __hash__(self):
        return hash(self.tuple)
    
    def __eq__(self, value):
        return self.tuple == value.tuple

    @cached_property
    def area(self):
        area = 0
        for p, v in self.items():
            if v == '#':
                area += 1
        return area

    def flip_v(self):
        values = reversed(self.values)
        return Present(values, self.origin)

    def flip_h(self):
        values = [reversed(row) for row in self.values]
        return Present(values, self.origin)

    def rotate_r(self):
        values = []
        for x in range(self.width):
            row = [r[x] for r in reversed(self.values)]
            values.append(row)
        return Present(values, self.origin)

    @cached_property
    def orientations(self):
        """
        All possible orientations:
        Rotations: 90, 180, 270
        Flip, then rotate again
        """
        if self.origin is not self:
            return self.origin.orientations
        orientations = set()
        cur = self
        orientations.add(cur)
        for _ in range(3):
            cur = cur.rotate_r()
            orientations.add(cur)
        cur = self.flip_v()
        orientations.add(cur)
        for _ in range(3):
            cur = cur.rotate_r()
            orientations.add(cur)
        return orientations


def readlines_stripped(path):
    with open(path, "r") as f:
        for line in f:
            yield line.rstrip('\r\n')


def load(path):
    state = 0
    presents = []
    regions = []
    for line in readlines_stripped(path):
        if state == 0:
            if line.endswith(':'):
                # starting a new present definition
                index = int(line[:-1])
                state = 1
                presents.insert(index, [])
                continue
            else:
                # presents are done, now we are defining regions
                state = 2
        elif state == 1:
            if not line:
                state = 0
                continue
            presents[index].append(line)
        # Not elif so we can fall through from state 0
        if state == 2:
            size, counts = line.split(':')
            width, length = (int(x) for x in size.split('x'))
            counts = [int(x) for x in counts.strip().split(' ')]
            regions.append((width, length, counts))

    presents = [Present(p) for p in presents]

    return presents, regions


def part1(path):
    presents, regions = load(path)
    for i, present in enumerate(presents):
        print(f'{i}:')
        for p in present.orientations:
            print(p.tuple)
            #print(str(p))
            #print()
    #print(regions)
    invalid_regions = 0
    exact_fit = 0
    for r, (width, length, counts) in enumerate(regions):
        region_area = width * length
        present_area = sum([presents[p].area * c for p, c in enumerate(counts)])
        if region_area < present_area:
            invalid_regions += 1
            #print(f'Region {r} too small ({region_area} <= {present_area})')
        elif region_area == present_area:
            exact_fit += 1
    print(f"Exact   regions: {exact_fit}")
    print(f"Invalid regions: {invalid_regions}")
    print(f"Valid   regions: {len(regions) - invalid_regions}")
    print(f"Total   regions: {len(regions)}")


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
