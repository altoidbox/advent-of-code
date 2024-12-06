import argparse
import re


def load(path):
    with open(path) as f:
        return f.read()


def part1(path):
    data = load(path)
    exp = r'mul\((\d+),(\d+)\)'
    total = 0
    for match in re.findall(exp, data):
        l, r = (int(x) for x in match)
        total += l * r
    print(total)


def part2(path):
    data = load(path)
    exp = r"(?:(do)\(\)|(don't)\(\)|(mul)\((\d+),(\d+)\))"
    total = 0
    enabled = True
    for match in re.findall(exp, data):
        action = match[0] or match[1] or match[2]
        if action == 'do':
            enabled = True
        elif action == "don't":
            enabled = False
        elif enabled:
            l, r = (int(x) for x in match[3:5])
            total += l * r
    print(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


main()
