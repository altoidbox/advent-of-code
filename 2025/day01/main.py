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
    return readlines_stripped(path)


def part1(path):
    data = load(path)
    count = 0
    pos = 50
    dir_map = { 'R': lambda n: int(n), 'L': lambda n: -int(n)}
    for move in data:
        pos += dir_map[move[0]](move[1:])
        pos %= 100
        if pos == 0:
            count += 1
    print(count)


def part2(path):
    data = load(path)
    count = 0
    pos = 50
    dir_map = { 'R': lambda n: int(n), 'L': lambda n: -int(n)}
    for move in data:
        start_pos = pos
        pos += dir_map[move[0]](move[1:])
        crosses0 = abs(pos) // 100
        if (pos < 0 and start_pos != 0) or pos == 0:
            crosses0 += 1
        #print(f'{start_pos} + {move} = {pos % 100}: {crosses0}')
        pos %= 100
        count += crosses0
    print(count)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
