import sys
from math import prod


def read_file(path):
    with open(path, "r") as f:
        return [s.strip() for s in f]


OPENS = '<([{'
CLOSES = '>)]}'
OPAIRS = { OPENS[i]: CLOSES[i] for i in range(len(OPENS)) }
CPAIRS = { CLOSES[i]: OPENS[i] for i in range(len(OPENS)) }
PAIRS = {}
PAIRS.update(OPAIRS)
PAIRS.update(CPAIRS)
CORRUPT_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
INCOMPLETE_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def score_corrupt(line):
    stack = []
    for c in line:
        if c in OPAIRS:
            stack.append(c)
            continue
        if len(stack) == 0:
            #print('Unmatched close:', c)
            return CORRUPT_SCORES[c]
        start = stack.pop()
        if start != CPAIRS[c]:
            #print('Incorrectly matched close:', start, c)
            return CORRUPT_SCORES[c]
    if len(stack) > 0:
        #print('Missing closes:', ''.join(stack))
        return 0
    return True


def score_incomplete(line):
    stack = []
    for c in line:
        if c in OPAIRS:
            stack.append(c)
            continue
        if len(stack) == 0:
            return 0
        start = stack.pop()
        if start != CPAIRS[c]:
            return 0
    score = 0
    while stack:
        score *= 5
        score += INCOMPLETE_SCORES[OPAIRS[stack.pop()]]
    return score


def part1(fname):
    data = read_file(fname)
    score = 0
    for line in data:
        score += score_corrupt(line)
    print(score)


def part2(fname):
    data = read_file(fname)
    scores = []
    for line in data:
        score = score_incomplete(line)
        if score:
            scores.append(score)
    print(sorted(scores)[len(scores)//2])


if __name__ == "__main__":
    part1(sys.argv[1])
    part2(sys.argv[1])
