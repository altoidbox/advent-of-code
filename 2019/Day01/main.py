import re


def read_file(path):
    with open(path, "r") as f:
        data = list(map(int, f))
    return data


def part1():
    data = read_file("input.txt")
    result = sum(map(lambda x: x//3 - 2, data))
    print("{} fuel".format(result))


def calc_fuel(fuel):
    result = 0
    last = fuel//3 - 2
    while last > 0:
        result += last
        last = last//3 - 2
    return result

def part2():
    data = read_file("input.txt")
    result = sum(map(calc_fuel, data))
    print("{} fuel".format(result))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
