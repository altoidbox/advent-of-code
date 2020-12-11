#FILE = "example.txt"
FILE = "input.txt"


def read_file(path):
    with open(path, "r") as f:
        data = list(map(lambda s: s.strip(), f))
    return data


def calc(data, right, down):
    i = 0
    result = 0
    d = down
    for line in data:
        d += 1
        if d < down:
            # print(line)
            continue
        d = 0
        if line[i % len(line)] == '#':
            result += 1
        # copy = bytearray(line, 'utf-8')
        # copy[i % len(line)] = ord('O')
        # print(copy.decode('utf-8'), line[i % len(line)])
        i += right
    return result


def part1():
    data = read_file(FILE)
    result = calc(data, 3, 1)
    print("{}".format(result))


def part2():
    data = read_file(FILE)
    result = calc(data, 1, 1) * calc(data, 3, 1) * calc(data, 5, 1) * calc(data, 7, 1) * calc(data, 1, 2)
    print("{}".format(result))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
