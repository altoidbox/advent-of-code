#!/usr/bin/env python3
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class Stacks(object):
    def __init__(self):
        self.stacks = {}
        self.model = 9000

    @staticmethod
    def parse(lst):
        ids = lst.pop()
        offsets = {}
        stacks = Stacks()
        for i, c in enumerate(ids):
            if c == ' ':
                continue
            c = int(c)
            stacks.stacks[c] = []
            offsets[i] = c
        #print(offsets)
        for line in reversed(lst):
            for offset, stack in offsets.items():
                item = line[offset]
                if item != ' ':
                    stacks.push(stack, item)
                #print(stack, stacks.stacks[stack])

        return stacks

    def push(self, stack, item):
        if isinstance(item, list):
            self.stacks[stack].extend(item)
        else:
            self.stacks[stack].append(item)
    
    def pop(self, stack, n):
        res = []
        stk = self.stacks[stack]
        for i in range(n):
            res.append(stk.pop())
        return list(reversed(res))

    def move(self, count, from_, to):
        print('move', count, 'from', from_, 'to', to)
        if self.model > 9000:
            self.push(to, self.pop(from_, count))
        else:
            for _ in range(count):
                self.push(to, self.pop(from_, 1))
    
    def __str__(self):
        lines = []
        line = ''
        for i in range(len(self.stacks)):
            line += ' {}  '.format(i+1)
        lines.append(line)

        idx = 0
        cont = True
        while cont:
            cont = False
            line = ''
            for i in range(len(self.stacks)):
                stack = self.stacks[i+1]

                if len(stack) > idx:
                    line += '[{}] '.format(stack[idx])
                    cont = True
                else:
                    line += '    '
            lines.append(line)
            idx += 1
        return '\n'.join(reversed(lines))
    

def load(args):
    stacks = []
    moves = []
    cur = stacks
    with open(args.input, 'r') as f:
        for line in f:
            line = line.strip('\r\n')
            if not line:
                cur = moves
                continue
            cur.append(line)
    stacks_obj = Stacks.parse(stacks)
    return stacks_obj, moves


def part1(data, model=9000):
    stacks, moves = data
    stacks.model = model
    for move in moves:
        match = re.match(r'move (\d+) from (\d+) to (\d+)', move)
        stacks.move(*[int(x) for x in match.groups()])
    print(stacks)
    ans = ''
    for i in range(len(stacks.stacks)):
        ans += str(stacks.stacks[i+1][-1])
    print(ans)


def part2(data):
    part1(data, 9001)


data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

