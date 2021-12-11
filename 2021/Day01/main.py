import argparse
from bisect import bisect_left


def read_file(path):
    with open(path, "r") as f:
        return list(map(int, f))


def binary_search(value, sorted_data):
    index = bisect_left(sorted_data, value)
    if index == len(sorted_data) or sorted_data[index] != value:
        return False
    return index


def part2():
    data = read_file("input.txt")
    cur = 0
    prev = 0
    count = 0
    for i in range(3):
        prev += data[i]
        cur += data[i+1]
    for i in range(3, len(data) - 1):
        if cur > prev:
            count += 1
        prev -= data[i-3]
        cur -= data[i-2]
        prev += data[i]
        cur += data[i+1]
    if cur > prev:
        count += 1
    print("{} increases".format(count))


def part1():
    data = read_file("input.txt")
    last = None
    count = 0
    for item in data:
        if last is not None and item > last:
            count += 1
        last = item
    print("{} increases".format(count))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()