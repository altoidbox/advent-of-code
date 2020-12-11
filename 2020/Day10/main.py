import argparse
from bisect import bisect_left
import itertools
from collections import defaultdict, deque


def read_file(path):
    with open(path, "r") as f:
        return list(map(int, f))


def part1(data):
    data = list(sorted(data))
    data.append(data[-1] + 3)
    prev = 0
    diffs = defaultdict(lambda: 0)
    for d in data:
        diffs[d - prev] += 1
        prev = d
    print(diffs[1] * diffs[3])
    return None


def solve_for(num, saved):
    count = 0
    for n in range(num + 1, num + 4):
        count += saved.get(n, 0)
    return count


def part2(data):
    data = list(sorted(data, reverse=True))
    saved = {data[0] + 3: 1}
    for value in data:
        saved[value] = solve_for(value, saved)
    print(solve_for(0, saved))


def run(path):
    data = read_file(path)
    part1(data)
    part2(data)


def main():
    run("example.txt")
    run("example2.txt")
    run("input.txt")


if __name__ == "__main__":
    main()
