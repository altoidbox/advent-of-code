import argparse
import re
from collections import OrderedDict, deque
import heapq
import sys


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class PrefixNode(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def delve(self, chr):
        if chr == '.':
            return self.left
        return self.right


class PrefixTree(object):
    def __init__(self, transforms):
        nodes = {key: PrefixNode(value == '#') for key, value in transforms.items()}
        for key in transforms.keys():
            node = nodes[key]
            node.left = nodes.get(key[1:] + '.')
            node.right = nodes[key[1:] + '#']
        self.nodes = nodes


class Puzzle(object):
    def __init__(self):
        self.initial_state = ''
        self.transforms = {}
        self.args = None

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("input")
        parser.add_argument("--part2", action="store_true")
        self.args = parser.parse_args()
        if args.part2:
            self.part2()
        else:
            self.part1()

    def read_input(self):
        with open(args.input, "r") as f:
            for line in f:
                match = re.match(r'([.#]+) => ([.#])', line)
                if match:
                    self.transforms[match.group(1)] = match.group(2)
                    continue
                match = re.match(r'initial state: +([.#]+)', line)
                if match:
                    self.initial_state = match.group(1)

    def do_transform(self, state, lindex):
        f_index = state.find('#')
        r_index = state.rfind('#')
        lindex += f_index - 2
        state = '....' + state[f_index:r_index+1] + '....'
        new_state = []
        for i in range(len(state) - 4):
            new_state.append(self.transforms.get(state[i:i+5], '.'))
        return ''.join(new_state), lindex

    def efficient_transform(self, empty_node, state, lindex):
        new_state = []
        lindex -= 2
        node = empty_node
        empty_len = 0
        for chr in state:
            node = node.delve(chr)
            if not node.value:
                empty_len += 1
            else:
                if len(new_state) == 0:
                    lindex += empty_len
                else:
                    new_state.extend(['.'] * empty_len)
                new_state.append('#')
                empty_len = 0
        if len(new_state) == 0:
            print("empty state!")
        new_state.extend(['.'] * empty_len)
        while node is not empty_node:
            node = node.delve('.')
            new_state.append('#' if node.value else '.')
        return new_state, lindex

    def part1(self):
        self.read_input()
        state = self.initial_state
        lindex = 0
        # print("{}: {}".format("0", state))
        for i in range(20):
            state, lindex = self.do_transform(state, lindex)
            # print("{}: {}".format(i + 1, state))
        count = 0
        for i, c in enumerate(state):
            count += 0 if c is '.' else (i + lindex)
        print(count)

    def part2(self):
        self.read_input()
        tree = PrefixTree(self.transforms)
        empty_node = tree.nodes['.....']
        state = list(self.initial_state)
        lindex = 0
        intervals = 20 if 'test' in self.args.input else 120
        count = 0
        for i in range(intervals):
            state, lindex = self.efficient_transform(empty_node, state, lindex)
            # print("{}: {}".format(i + 1, ''.join(state)))
            prev_count = count
            count = 0
            for idx, c in enumerate(state):
                count += 0 if c is '.' else (idx + lindex)
            print(i, lindex, len(state), count, count - prev_count)
            if i > 110:
                print(i, 10614 + (i - 110) * 87)
        print(10614 + (50000000000 - 111) * 87)


Puzzle().parse_args()
