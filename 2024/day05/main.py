#!/usr/bin/env python3

import argparse
from collections import defaultdict
from functools import cmp_to_key


def load(path):
    rules = []
    updates = []
    cur = rules
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                cur = updates
                continue
            cur.append(line)
    for i, rule in enumerate(rules):
        rules[i] = tuple(int(x) for x in rule.split('|'))
    for i, update in enumerate(updates):
        updates[i] = tuple(int(x) for x in update.split(','))
    return rules, updates


def is_valid(ruleset, update):
    encountered = set()
    for item in update:
        intersect = ruleset[item].intersection(encountered)
        if intersect:
            #print(f"{item} violates {intersect}")
            return False
        encountered.add(item)
    return True


def part1(path):
    rules, updates = load(path)
    ruleset = defaultdict(set)
    for before, after in rules:
        ruleset[before].add(after)
    total = 0
    for update in updates:
        if is_valid(ruleset, update):
            middle = update[len(update) // 2]
            #print(f"{middle} from {update}")
            total += middle
    print(total)


def mk_compare(ruleset):
    def compare(a, b):
        nonlocal ruleset
        if b in ruleset[a]:
            return -1
        if a in ruleset[b]:
            return 1
        return 0
    return compare


def part2(path):
    rules, updates = load(path)
    ruleset = defaultdict(set)
    for before, after in rules:
        ruleset[before].add(after)
    bad = []
    for update in updates:
        if not is_valid(ruleset, update):
            bad.append(update)
    compare = mk_compare(ruleset)
    total = 0
    for update in bad:
        correct = list(sorted(update, key=cmp_to_key(compare)))
        middle = correct[len(correct) // 2]
        total += middle
    print(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)

if __name__ == '__main__':
    main()
