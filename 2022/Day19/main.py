#!/usr/bin/env python3
import argparse
import re
import functools

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class Blueprint(object):
    def __init__(self, num):
        self.num = num
        self.robots = {}
    
    def __repr__(self):
        return '{}: {}'.format(self.num, self.robots)


def load(path):
    blueprints = []
    with open(args.input, "r") as f:
        for line in f:
            match = re.search(r'Blueprint (\d+)', line)
            if match:
                blueprints.append(Blueprint(int(match.group(1))))
            match = re.search(r'Each (ore) robot costs (\d+) (\w+).', line)
            if match:
                blueprints[-1].robots[match.group(1)] = { match.group(3): int(match.group(2)) }
            match = re.search(r'Each (clay) robot costs (\d+) (\w+).', line)
            if match:
                blueprints[-1].robots[match.group(1)] = { match.group(3): int(match.group(2)) }
            match = re.search(r'Each (obsidian) robot costs (\d+) (\w+) and (\d+) (\w+).', line)
            if match:
                blueprints[-1].robots[match.group(1)] = { 
                    match.group(3): int(match.group(2)),
                    match.group(5): int(match.group(4))
                }
            match = re.search(r'Each (geode) robot costs (\d+) (\w+) and (\d+) (\w+).', line)
            if match:
                blueprints[-1].robots[match.group(1)] = { 
                    match.group(3): int(match.group(2)),
                    match.group(5): int(match.group(4))
                }
            
    return blueprints


def simulate(bp):
    pass


def part1(data):
    print(data)


def part2(data):
    pass

data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

