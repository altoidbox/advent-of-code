#!/usr/bin/env python3
import argparse
import re
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def load(path):
    data = deque()
    with open(args.input, "r") as f:
        for line in f:
            data.append(line.strip())
    return data


class Monkey(object):
    def __init__(self, id_):
        self.id = id_
        self.items = deque()
        self.operate = lambda item: item
        self.modulus = 0
        self.worry_divisor = 3
        self.targets = [-1, -1]
        self.count = 0

    def test(self, item):
        return (item % self.modulus) == 0

    def process(self):
        item = self.items.popleft()
        #print("  Monkey inspects an item with a worry level of {}.".format(item))
        item = self.operate(item)
        #print("    Worry level is increased to {}.".format(item))
        item //= self.worry_divisor
        #print("    Monkey gets bored with item. Worry level is divided by 3 to {}.".format(item))
        result = self.test(item)
        #print("    Current worry level is{} divisible by {}.".format('' if result else ' not', self.modulus))
        target = self.targets[int(self.test(item))]
        #print("    Item with worry level {} is thrown to monkey {}.".format(item, target))
        self.count += 1
        return target, item

    @staticmethod
    def parse(lines):
        while True:
            match = re.match(r'Monkey (\d+):', lines.popleft())
            if match:
                break
        m = Monkey(int(match.group(1)))
        match = re.search(r'Starting items: (.+)', lines.popleft())
        for item in match.group(1).split(', '):
            m.items.append(int(item))
        match = re.search(r'Operation: new = (\S+ . \S+)', lines.popleft())
        m.operate = eval('lambda old: ' + match.group(1))
        match = re.search(r'Test: divisible by (\d+)', lines.popleft())
        m.modulus = int(match.group(1))
        match = re.search(r'If true: throw to monkey (\d+)', lines.popleft())
        m.targets[int(True)] = int(match.group(1))
        match = re.search(r'If false: throw to monkey (\d+)', lines.popleft())
        m.targets[int(False)] = int(match.group(1))
        return m


def print_summary(monkeys):
    for m in monkeys:
        #print("Monkey {}: {}".format(m.id, m.items))
        print("Monkey {} inspected {}".format(m.id, m.count))


def part1(data):
    monkeys = []
    while(data):
        monkeys.append(Monkey.parse(data))
    for _ in range(20):
        for m in monkeys:
            #print("Monkey {}:".format(m.id))
            while m.items:
                target, item = m.process()
                monkeys[target].items.append(item)
    ordered = sorted(monkeys, key=lambda m: m.count)
    print_summary(monkeys)
    print(ordered[-1].count * ordered[-2].count)


def part2(data):
    monkeys = []
    modulus = 1
    while(data):
        m = Monkey.parse(data)
        monkeys.append(m)
        m.worry_divisor = 1
        modulus *= m.modulus
    print(modulus)
    for _ in range(10000):
        for m in monkeys:
            while m.items:
                target, item = m.process()
                monkeys[target].items.append(item % modulus)
    ordered = sorted(monkeys, key=lambda m: m.count)
    print_summary(monkeys)
    print(ordered[-1].count * ordered[-2].count)
    

data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

