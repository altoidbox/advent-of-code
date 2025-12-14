#!/usr/bin/env python3

import argparse
import argparse
from pathlib import Path
import sys
import random
import math


# Add the common directory to the path
SCRIPT_DIR = Path(__file__).absolute().parent
sys.path.append(str(SCRIPT_DIR.parent.parent))


import common
from common.point import Point3D
from common.debug import dprint


def readlines_stripped(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.rstrip('\r\n')
            data.append(line)
    return data


def load(path):
    points = []
    for line in readlines_stripped(path):
        points.append(Point3D(*(int(i) for i in line.split(','))))
    return points


def round_point(p, d):
    return Point3D(*(int(s // d) for s in p.dims))


def find_closest_pair(points: list[Point3D]):
    # Step 1: Randomly select n pairs of points and find the closest distance
    min_dist = math.inf
    min_pair = None
    for _ in range(len(points)):
        # choose the first point, by index
        i1 = random.randrange(len(points))
        # choose the one to pair, with 1 fewer option
        i2 = random.randrange(len(points) - 1)
        # if the index is the same or greater than the first, increment
        if i2 >= i1:
            i2 += 1
        dist = points[i1].euclidean_dist(points[i2])
        if dist < min_dist:
            min_dist = dist
            min_pair = i1, i2
    # Step 2: "Round" each point into a grid of size min_dist, 
    #   and insert the point into a hash table based on this rounded point
    grid = {}
    rounded_points = []
    for i, p in enumerate(points):
        rp = round_point(p, min_dist)
        rounded_points.append(rp)
        grid.setdefault(rp, []).append(i)
    # Step 3: For each point, compare it with each other point in the surrounding
    #   grid squares (Moore Neighborhood + same grid square)
    for i, (p, rp) in enumerate(zip(points, rounded_points)):
        for adacent_rp in rp.adjacent(include_self=True):
            for neighbor_i in grid.get(adacent_rp, []):
                if neighbor_i == i:
                    continue
                dist = p.euclidean_dist(points[neighbor_i])
                if dist < min_dist:
                    min_dist = dist
                    min_pair = i, neighbor_i

    return min_dist, min_pair


def find_closest_nonjoined_pair(points: list[Point3D], joined: set[tuple[int, int]]):
    # Step 1: Randomly select n pairs of points and find the closest distance
    min_dist = math.inf
    min_pair = None
    for i in range(len(points)):
        # choose the first point, by index
        i1 = random.randrange(len(points))
        # choose the one to pair, with 1 fewer option
        i2 = random.randrange(len(points) - 1)
        # if the index is the same or greater than the first, increment
        if i2 >= i1:
            i2 += 1
        if (i1, i2) in joined:
            continue
        dist = points[i1].euclidean_dist(points[i2])
        if dist < min_dist:
            min_dist = dist
            min_pair = i1, i2
    # Step 2: "Round" each point into a grid of size min_dist, 
    #   and insert the point into a hash table based on this rounded point
    grid = {}
    rounded_points = []
    for i, p in enumerate(points):
        rp = round_point(p, min_dist)
        rounded_points.append(rp)
        grid.setdefault(rp, []).append(i)
    # Step 3: For each point, compare it with each other point in the surrounding
    #   grid squares (Moore Neighborhood + same grid square)
    for i, (p, rp) in enumerate(zip(points, rounded_points)):
        for adacent_rp in rp.adjacent(include_self=True):
            for neighbor_i in grid.get(adacent_rp, []):
                if neighbor_i == i:
                    continue
                if (i, neighbor_i) in joined:
                    continue
                dist = p.euclidean_dist(points[neighbor_i])
                if dist < min_dist:
                    min_dist = dist
                    min_pair = i, neighbor_i

    return min_dist, min_pair


def join_pair(i1, i2, joined, circuits):
    # Update our joined set with the new pair, in both directions to make lookup easier
    joined.add((i1, i2))
    joined.add((i2, i1))
    # merge the circuits that each end of the pair is in
    c1 = circuits[i1]
    c2 = circuits[i2]
    if c1 is c2:
        # If they are already in the same circuit, there's nothing more to do
        dprint('    already in same circuit')
        return
    dprint(f'    merging set of len {len(c1)} with set of len {len(c2)}')
    # For some sort of efficiency, add the smaller set to the larger, and update all the references
    if len(c2) > len(c1):
        c1, c2 = c2, c1
    c1.update(c2)
    for i in c2:
        circuits[i] = c1
    # Detect when all points have merged into the same circuit
    return len(c1) == len(circuits)


def join_closest(points, count):
    # Start with nothing joined
    joined = set()
    # Each junction box is a circuit of just one, itself
    circuits = [{i} for i in range(len(points))]
    for i in range(count):
        md, (i1, i2) = find_closest_nonjoined_pair(points, joined)
        dprint('join', points[i1], points[i2], 'dist', md)
        join_pair(i1, i2, joined, circuits)

    top3 = sorted({id(c): c for c in circuits}.values(), key=lambda c: len(c), reverse=True)[:3]
    print(top3)
    print(math.prod((len(c) for c in top3)))


def find_candidate_minimum_distances(points):
    # Step 1: Randomly select n pairs of points and find the closest distance
    distances = []
    for i in range(len(points)):
        # choose the first point, by index
        i1 = random.randrange(len(points))
        # choose the one to pair, with 1 fewer option
        i2 = random.randrange(len(points) - 1)
        # if the index is the same or greater than the first, increment
        if i2 >= i1:
            i2 += 1
        else:
            i1, i2 = i2, i1
        dist = points[i1].euclidean_dist(points[i2])
        distances.append(dist)
    # We will use this calculation throughout
    return sorted(distances)


def round_points(points, min_dist):
    # Step 2: "Round" each point into a grid of size min_dist, 
    #   and insert the point into a hash table based on this rounded point
    grid = {}
    rounded_points = []
    for i, p in enumerate(points):
        rp = round_point(p, min_dist)
        rounded_points.append(rp)
        grid.setdefault(rp, []).append(i)
    return grid, rounded_points


def find_closest_nonjoined_pairs(points: list[Point3D], joined: set[tuple[int, int]], grid, rounded_points, grid_size):
    # Step 3: For each point, compare it with each other point in the surrounding
    #   grid squares (Moore Neighborhood + same grid square)
    # In this modification, we will find all pairs closer than grid_size
    min_points = []
    for i, (p, rp) in enumerate(zip(points, rounded_points)):
        for adacent_rp in rp.adjacent(include_self=True):
            for neighbor_i in grid.get(adacent_rp, []):
                if neighbor_i <= i:
                    # Don't compare a point to itself
                    # Also, only consider pairs where neighbor_i > i
                    continue
                if (i, neighbor_i) in joined:
                    # if a pair is already joined, ignore them
                    continue
                dist = p.euclidean_dist(points[neighbor_i])
                if dist <= grid_size:
                    min_points.append((dist, (i, neighbor_i)))

    return min_points


def better_join_closest(points, count):
    joined = set()
    circuits = [{i} for i in range(len(points))]
    closest = []
    dlist = find_candidate_minimum_distances(points)
    dprint(dlist)
    while len(closest) < count:
        d = dlist.pop(0)
        dprint(d)
        grid, rounded_points = round_points(points, d)
        cur_closest = find_closest_nonjoined_pairs(points, joined, grid, rounded_points, d)
        for d, (i1, i2) in sorted(cur_closest):
            join_pair(i1, i2, joined, circuits)
            closest.append((d, (i1, i2)))
            if len(closest) == count:
                break
    top3 = sorted({id(c): c for c in circuits}.values(), key=lambda c: len(c), reverse=True)[:3]
    print(top3)
    print(math.prod((len(c) for c in top3)))


def part1(path):
    target = 10
    points = load(path)
    #join_closest(points, target)
    better_join_closest(points, target)


def part2(path):
    points = load(path)
    #join_closest(points, target)
    #better_join_closest(points, target)
    all_pairs = []
    for i1 in range(len(points)):
        for i2 in range(i1 + 1, len(points)):
            all_pairs.append((points[i1].euclidean_dist(points[i2]), (i1, i2)))
    all_pairs.sort()
    circuits = [{i} for i in range(len(points))]
    joined = set()
    pidx = 0
    while len(circuits[0]) < len(points):
        d, (i1, i2) = all_pairs[pidx]
        join_pair(i1, i2, joined, circuits)
        if pidx == 0:
            print(d)
        pidx += 1
    print(points[i1], points[i2], d, pidx)
    print(points[i1].x * points[i2].x)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--debug', '-d', action='store_true')
    args = parser.parse_args()
    if args.debug:
        common.debug.DEBUG = True
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
