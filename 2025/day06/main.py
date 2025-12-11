#!/usr/bin/env python3

import argparse
import re

def readlines_stripped(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.rstrip('\r\n')
            data.append(line)
    return data


def load(path):
    cols = []
    for line in readlines_stripped(path):
        cols.append(re.findall(r'[^ ]+', line))
    return cols


def part1(path):
    data = load(path)
    operations = data[-1]
    numbers = data[:-1]
    total = 0
    for i, op in enumerate(operations):
        if op == '*':
            value = 1
            opf = lambda x, y: x * y
        elif op == '+':
            value = 0
            opf = lambda x, y: x + y
        for row in numbers:
            value = opf(value, int(row[i]))
        total += value
    print(total)


def get_column(rows, col):
    return ''.join(row[col] for row in rows).strip()


def part2(path):
    data = readlines_stripped(path)
    operations = data[-1]
    numbers = data[:-1]
    total = 0
    for i, op in enumerate(operations):
        if op == '*':
            value = 1
            opf = lambda x, y: x * y
        elif op == '+':
            value = 0
            opf = lambda x, y: x + y
        col_data = get_column(numbers, i)
        if not col_data:
            total += value
            value = 0
            continue
        value = opf(value, int(col_data))
    total += value
    print(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
