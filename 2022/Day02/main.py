#!/usr/bin/env python3
import argparse
import heapq

parser = argparse.ArgumentParser()
parser.add_argument("input", default='input.txt')
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()

TABLE = {
    'A': 'ZXY',
    'B': 'XYZ',
    'C': 'YZX'
}

def play(opp, mine):
    score = ord(mine) - ord('X') + 1
    win = TABLE[opp].index(mine) * 3
    print(opp, mine, score, win, score + win)
    return score + win


def parse(args):
    rounds = []
    with open(args.input, 'r') as f:
        for line in f:
            line = line.strip()
            rounds.append(line.split())
    return rounds


def part1(args):
    rounds = parse(args)
    print("\nFinal Result1: {}".format(sum(play(*rnd) for rnd in rounds)))


def play2(opp, outcome):
    result = ord(outcome) - ord('X')
    win = result * 3
    mine = chr(ord(TABLE[opp][result]) - ord('X') + ord('A'))
    score = ord(mine) - ord('A') + 1
    print(opp, mine, score, win, score + win)
    return score + win


def part2(args):
    rounds = parse(args)
    print("\nFinal Result1: {}".format(sum(play2(*rnd) for rnd in rounds)))


if not args.part2:
    part1(args)
else:
    part2(args)

