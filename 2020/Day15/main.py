import re

FILE = "input.txt"
# FILE = "example1.txt"
# FILE = "example2.txt"


def read_file(path):
    with open(path, "r") as f:
        return list(map(int, f.read().split(',')))


def part1():
    data = read_file(FILE)
    prev_map = {}
    for i in data[:-1]:
        prev_map[i] = len(prev_map)
        # print(prev_map[i], last_spoken, None)
    last_spoken = data[-1]
    # print(len(prev_map), last_spoken, None)
    for i in range(len(prev_map), 2020 - 1):
        when_spoken = prev_map.get(last_spoken, None)
        prev_map[last_spoken] = i
        if when_spoken is None:
            last_spoken = 0
        else:
            last_spoken = i - when_spoken
        # print(i + 1, last_spoken, when_spoken)
    print(last_spoken)


def part2():
    data = read_file(FILE)
    prev_map = {}
    for i in data[:-1]:
        prev_map[i] = len(prev_map)
    last_spoken = data[-1]
    for i in range(len(prev_map), 30000000 - 1):
        when_spoken = prev_map.get(last_spoken, None)
        prev_map[last_spoken] = i
        if when_spoken is None:
            last_spoken = 0
        else:
            last_spoken = i - when_spoken
    print(last_spoken)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
