
def read_file(path):
    with open(path, "r") as f:
        return list(map(int, f.readline().split(',')))


def calc_fuel(values, target):
    cost = 0
    for v in values:
        cost += int(abs(v - target))
    return cost


def part1():
    values = read_file('input.txt')
    print("{} - {}, avg: {}".format(min(values), max(values), sum(values) / len(values)))
    print(min(calc_fuel(values, i) for i in range(len(values))))


def summation(n):
    return (n * (n + 1)) // 2


def calc_fuel2(values, target):
    cost = 0
    for v in values:
        cost += summation(int(abs(v - target)))
    return cost


def part2():
    values = read_file('input.txt')
    print("{} - {}, avg: {}".format(min(values), max(values), sum(values) / len(values)))
    print(min(calc_fuel2(values, i) for i in range(len(values))))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
