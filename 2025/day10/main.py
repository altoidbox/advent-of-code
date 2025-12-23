#!/usr/bin/env python3

import argparse
import argparse
from pathlib import Path
import sys
from itertools import combinations


# Add the common directory to the path
SCRIPT_DIR = Path(__file__).absolute().parent
sys.path.append(str(SCRIPT_DIR.parent.parent))


def readlines_stripped(path):
    with open(path, "r") as f:
        for line in f:
            yield line.rstrip('\r\n')


def load(path):
    for line in readlines_stripped(path):
        parts = line.split(' ')
        lights = [i == '#' for i in parts[0][1:-1]]
        buttons = []
        for button in parts[1:-1]:
            buttons.append(tuple(int(x) for x in button[1:-1].split(',')))
        joltage = parts[-1]
        yield((lights, buttons, joltage))


def solve1(lights, buttons):
    # This appears to be an xor. What values (buttons) do we xor together to get the light output
    # Since a value xor itself results in no change, it never really makes sense to use the same value more than once
    goal = 0
    for i, t in enumerate(reversed(lights)):
        goal |= (1 << i) if t else 0
    for i, btn in enumerate(buttons):
        buttons[i] = sum(1 << (len(lights) - v - 1) for v in btn)
    
    for answer in range(len(buttons)):
        for combo in combinations(buttons, answer):
            value = 0
            for btn in combo:
                value ^= btn
            if value == goal:
                return answer
    btnstr = ', '.join(f'{btn:0{len(lights)}b}' for btn in buttons)
    print(f'No answer: {goal:0{len(lights)}b} ({btnstr})')


def part1(path):
    value = 0
    for lights, buttons, _ in load(path):
        value += solve1(lights, buttons)
    print(value)


def part2(path):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
