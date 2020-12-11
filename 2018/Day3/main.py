import argparse
import re
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def read_input(path):
    items = OrderedDict()
    with open(path, "r") as f:
        for line in f:
            # #1 @ 604,670: 22x16
            match = re.match(r'#(\d+) +@ +(\d+),(\d+): (\d+)x(\d+)', line)
            fields = tuple(map(int, match.groups()))
            # claim, left, top, width, height = match.groups()
            items[fields[0]] = fields[1:]
    return items


def empty_cloth(width, height):
    cloth = []
    for _ in range(height):
        cloth.append([0] * width)
    return cloth


def mark_cloth(cloth, left, top, width, height):
    for h in range(top, top + height):
        for w in range(left, left + width):
            cloth[h][w] += 1


def check_claim(cloth, left, top, width, height):
    for h in range(top, top + height):
        for w in range(left, left + width):
            if cloth[h][w] != 1:
                return False
    return True


def part1(args):
    cloth = empty_cloth(1000, 1000)
    claims = read_input(args.input)
    for claim in claims.values():
        mark_cloth(cloth, *claim)
    overlap = 0
    for row in cloth:
        for entry in row:
            if entry > 1:
                overlap += 1
    print("{} sq. inches of overlap".format(overlap))


def part2(args):
    cloth = empty_cloth(1000, 1000)
    claims = read_input(args.input)
    for claim in claims.values():
        mark_cloth(cloth, *claim)
    for claim_id, claim in claims.items():
        if check_claim(cloth, *claim):
            print("Claim {} has no overlap".format(claim_id))


if args.part2:
    part2(args)
else:
    part1(args)
