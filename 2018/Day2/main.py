import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def part1(args):
    counts = {}
    counts[2] = 0
    counts[3] = 0
    with open(args.input, 'rb') as f:
        for line in f:
            keys = {}
            for char in line.strip():
                keys[char] = keys.setdefault(char, 0) + 1
            for value in (2, 3):
                if any(v == value for v in keys.values()):
                    counts[value] += 1
                    print("{} has {} of one character".format(line, value))

    result = counts[2] * counts[3]
    print("\nFinal Result: {}".format(result))


def part2(args):
    items = []
    with open(args.input, "r") as f:
        for line in f:
            items.append(line.strip())
    for i in items:
        for j in items:
            diff = -1
            for idx, s in enumerate(map(lambda l, r: {l, r}, i, j)):
                if len(s) > 1:
                    if diff != -1:
                        diff = -1
                        break
                    diff = idx
            if diff != -1:
                print("Found {}/{} = {}".format(i, j, i[:diff] + i[diff+1:]))


if not args.part2:
    part1(args)
else:
    part2(args)

