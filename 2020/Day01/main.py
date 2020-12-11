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
    data = sorted(read_file("input.txt"))
    for li, l in enumerate(data):
        for ri, r in enumerate(reversed(data)):
            ri = len(data) - ri - 1
            if li >= ri:
                break
            # print(li, ri, l, r, l+r)
            target = 2020 - (l + r)
            if target < 0:
                continue
            elif binary_search(target, data) is not False:
                print("{} * {} * {} == {}".format(l, r, target, l * r * target))
                return
    print("Not found")


def part1():
    data = sorted(read_file("input.txt"))
    for li, l in enumerate(data):
        for ri, r in enumerate(reversed(data)):
            ri = len(data) - ri - 1
            if li >= ri:
                break
            # print(li, ri, l, r, l+r)
            added = l + r
            if added > 2020:
                continue
            elif added == 2020:
                print("{} * {} == {}".format(l, r, l * r))
                return
            else:
                break
    print("Not found")


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()