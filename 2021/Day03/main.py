
def read_file(path):
    with open(path, "r") as f:
        return list(line.strip() for line in f)


def bin2int(bin):
    value = 0
    for i, v in enumerate(reversed(bin)):
        if v == '1':
            value += 2 ** i
    return value


def part1():
    data = read_file('input.txt')
    items = [{'0': 0, '1': 0} for _ in data[0]]
    for item in data:
        for i, v in enumerate(item):
            items[i][v] += 1
    gamma = 0
    for i, d in enumerate(reversed(items)):
        if d['1'] > d['0']:
            gamma += 2 ** i
    epsilon = ~gamma & (2 ** len(data[0]) - 1)
    print(gamma, epsilon, gamma * epsilon)


def most_common(data, index):
    items = {'0': [], '1': []}
    for item in data:
        items[item[index]].append(item)
    if len(items['1']) >= len(items['0']):
        return items['1'], items['0']
    return items['0'], items['1']


def part2():
    data = read_file('input.txt')
    o2, co2 = most_common(data, 0)
    i = 0
    while len(o2) > 1:
        i += 1
        o2, _ = most_common(o2, i)
    #print(i, o2)
    i = 0
    while len(co2) > 1:
        i += 1
        _, co2 = most_common(co2, i)
    #print(i, co2)
    print(bin2int(o2[0]), bin2int(co2[0]), bin2int(o2[0]) * bin2int(co2[0]))


def main():
    part2()


if __name__ == "__main__":
    main()
