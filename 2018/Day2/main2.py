import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def part1(args):
    pass


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



if args.part2:
    part2(args)
else:
    part1(args)
