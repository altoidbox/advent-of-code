import argparse
from datetime import datetime
import re
from collections import deque
import heapq


def yc(point):
    return point[1]


def xc(point):
    return point[0]


def zc(point):
    return point[2]


def add_points(left, right):
    return left[0] + right[0], left[1] + right[1], left[2] + right[2]


def dist_points(left, right):
    return abs(right[0] - left[0]) + abs(right[1] - left[1]) + abs(right[2] - left[2])


def range_overlap(lp, lr, rp, rr):
    return dist_points(lp, rp) <= lr + rr


def overlap_size(lp, lr, rp, rr):
    return lr + rr - dist_points(lp, rp)


def mid_point(lp, rp):
    return (lp[0] + rp[0]) // 2, (lp[1] + rp[1]) // 2, (lp[2] + rp[2]) // 2


NEG_ADJACENTS = ((-1, 0, 0), (0, -1, 0), (0, 0, -1))

ADJACENTS = (
    (-1, 0, 0), (0, -1, 0), (0, 0, -1),
    (1, 0, 0), (0, 1, 0), (0, 0, 1))


def get_adjacents(grid, point, type_):
    values = []
    for offs in ADJACENTS:
        p = add_points(point, offs)
        if grid.get(p) == type_:
            values.append(p)
    return values


class Bounds(object):
    def __init__(self, points):
        self.minx = min(p[0] for p in points)
        self.maxx = max(p[0] for p in points)
        self.miny = min(p[1] for p in points)
        self.maxy = max(p[1] for p in points)

    def xrange(self):
        return range(self.minx, self.maxx + 1)

    def yrange(self):
        return range(self.miny, self.maxy + 1)

    @property
    def width(self):
        return self.maxx - self.minx + 1

    @property
    def height(self):
        return self.maxy - self.miny + 1


class BoundedGrid(object):
    def __init__(self, bounds):
        self.bounds = bounds
        self.grid = []
        for _ in range(bounds.maxx - bounds.minx + 1):
            self.grid.append([None] * (bounds.maxy - bounds.miny + 1))
        self.set_elements = 0

    def contains(self, point):
        return self.bounds.minx <= point.x <= self.bounds.maxx and self.bounds.miny <= point.y <= self.bounds.maxy

    def get(self, point):
        return self.grid[point.x - self.bounds.minx][point.y - self.bounds.miny]

    def set(self, point, item):
        self.grid[point.x - self.bounds.minx][point.y - self.bounds.miny] = item


def read_input(input):
    data = {}
    with open(input, 'r') as f:
        for line in f:
            # pos=<26057576,-10751309,46491633>, r=91461401
            x, y, z, r = map(int, re.match(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)', line).groups())
            data[(x, y, z)] = r
    return data


def part1(args):
    data = read_input(args.input)
    sp, sr = max(data.items(), key=lambda e: e[1])
    in_range = 0
    for point, r in data.items():
        if dist_points(sp, point) <= sr:
            in_range += 1
    print(in_range)


def circle_corners(point, distance):
    return [
        add_points(point, (distance, 0, 0)),
        add_points(point, (-distance, 0, 0)),
        add_points(point, (0, distance, 0)),
        add_points(point, (0, -distance, 0)),
        add_points(point, (0, 0, distance)),
        add_points(point, (0, 0, -distance)),
    ]


def num_in_range(data, point):
    count = 0
    for rp, rr in data.items():
        if range_overlap(point, 0, rp, rr):
            count += 1
    return count


import z3


def zabs(x):
    return z3.If(x >= 0, x, -x)


def part2(args):
    data = read_input(args.input)
    print(min(data.values()))
    return
    data_list = list(data.items())
    x, y, z = (z3.Int('x'), z3.Int('y'), z3.Int('z'))
    in_ranges = [
        z3.Int('in_range_' + str(i)) for i in range(len(data_list))
    ]
    range_count = z3.Int('sum')
    o = z3.Optimize()
    for i, ((nx, ny, nz), rng) in enumerate(data_list):
        o.add(in_ranges[i] == z3.If(zabs(x-nx) + zabs(y-ny) + zabs(z-nz) <= rng, 1, 0))
    o.add(range_count == sum(in_ranges))
    dist_from_zero = z3.Int('dist')
    o.add(dist_from_zero == zabs(x) + zabs(y) + zabs(z))
    h1 = o.maximize(range_count)
    h2 = o.minimize(dist_from_zero)
    o.check()
    m = o.model()
    print(m.eval(x), m.eval(y), m.eval(z))
    print(o.upper(h1))
    print(o.lower(h2))
    return
    all_in_range = {}
    for lp, lr in data.items():
        in_range = set()
        for rp, rr in data.items():
            if range_overlap(lp, lr, rp, rr):
                in_range.add(rp)
        all_in_range[lp] = in_range

    by_neighbors = {}
    for point, range_set in all_in_range.items():
        by_neighbors.setdefault(len(range_set), []).append(point)
        # print("{}: {}".format(point, range_set))
    max_neighbors = max(by_neighbors.keys())
    best = min(by_neighbors[max_neighbors], key=lambda point: dist_points((0, 0, 0), point))
    best_range = data[best]
    print("{} has {} points in range, including itself".format(best, max_neighbors))

    corner_ranges = {}
    for lp, lr in data.items():
        for corner in circle_corners(lp, lr):
            in_range = set()
            for rp, rr in data.items():
                if range_overlap(corner, 0, rp, rr):
                    in_range.add(rp)
            corner_ranges[corner] = in_range
    best_corner = max(corner_ranges.keys(), key=lambda point: len(corner_ranges[point]))
    print("best corner: {}, {} neighbors".format(best_corner, len(corner_ranges[best_corner])))

    best_count = len(corner_ranges[best_corner])
    while True:
        old_best = best_corner
        for offs in NEG_ADJACENTS:
            point = add_points(best_corner, offs)
            count = num_in_range(data, point)
            if count >= best_count:
                best_count = count
                best_corner = point
                break
        if old_best == best_corner:
            break
        print("best point: {}, {} neighbors".format(best_corner, best_count))
    print(dist_points((0, 0, 0), best_corner))

    return
    pass
    by_overlap_size = {}
    for point in all_in_range[best]:
        by_overlap_size.setdefault(overlap_size(best, data[best], point, data[point]), []).append(point)
        # print("{}: {}".format(point, range_set))
    min_overlap = min(by_overlap_size.keys())
    print("Min overlapping points: {} overlap {}".format(min_overlap, by_overlap_size[min_overlap]))
    other = by_overlap_size[min_overlap][0]

    mid = mid_point(best, other)
    corners = [
        add_points(mid, (min_overlap // 2, 0, 0)),
        add_points(mid, (-min_overlap // 2, 0, 0)),
        add_points(mid, (0, min_overlap // 2, 0)),
        add_points(mid, (0, -min_overlap // 2, 0)),
        add_points(mid, (0, 0, min_overlap // 2)),
        add_points(mid, (0, 0, -min_overlap // 2)),
    ]
    for target in corners:
        count = 0
        for point, rng in data.items():
            if dist_points(target, point) <= rng:
                count += 1
        print("range edge {} in range of {} points".format(target, count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--part2", action="store_true")

    args = parser.parse_args()

    if args.part2:
        part2(args)
    else:
        part1(args)
