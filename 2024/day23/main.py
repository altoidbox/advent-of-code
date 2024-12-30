#!/usr/bin/env python3

import argparse
from collections import defaultdict


def load(path):
    with open(path, "r") as f:
        data = [line.strip().split('-') for line in f]
    return data


def part1(path):
    data = load(path)
    edges = defaultdict(set)
    for a, b in data:
        edges[a].add(b)
        edges[b].add(a)
    groups = set()
    #while edges:
    #    group = set()
    #    stack = set([next(iter(edges))])
    #    while stack:
    #        node = stack.pop()
    #        group.add(node)
    #        stack.update(edges.pop(node) - group)
    #    groups.append(group)
    for node, connections in edges.items():
        #network = tuple(sorted(connections.union([node])))
        for conn in connections:
            candidates = edges[conn].intersection(connections)
            for cand in candidates:
                groups.add(tuple(sorted([node, conn, cand])))
    count = 0
    for g in sorted(groups):
        for n in g:
            if n.startswith('t'):
                count += 1
                break
    print(count)


VISITED = set()


def find_network(edges, node, group):
    copy = group.copy()
    copy.add(node)
    key = tuple(sorted(copy))
    if key in VISITED:
        return
    VISITED.add(key)
    for conn in edges[node]:
        candidates = edges[node].intersection(*(edges[g] for g in group))
        if len(candidates) == 0:
            #print(node, conn, sorted(copy))
            continue
        for cand in candidates:
            find_network(edges, cand, copy)


def part2(path):
    data = load(path)
    edges = defaultdict(set)
    for a, b in data:
        edges[a].add(b)
        edges[b].add(a)
    for node, connections in edges.items():
        find_network(edges, node, set())
    result = max(VISITED, key=len)
    print(','.join(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
