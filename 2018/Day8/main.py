import argparse
import re
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class Node(object):
    def __init__(self):
        self.children = []
        self.metadata = []
        self._value = None

    def walk(self, func, *args, **kwargs):
        func(self, *args, **kwargs)
        for child in self.children:
            child.walk(func, *args, **kwargs)

    @property
    def value(self):
        if self._value is not None:
            return self._value
        if len(self.children) == 0:
            self._value = sum(self.metadata)
        else:
            value = 0
            for idx in self.metadata:
                idx -= 1
                if idx < 0:
                    continue
                try:
                    value += self.children[idx].value
                except IndexError:
                    pass
            self._value = value
        return self._value

    @staticmethod
    def load(data, idx=0):
        self = Node()
        num_children = data[idx]
        num_metadata = data[idx+1]
        skip = 2
        for _ in range(num_children):
            child, eaten = Node.load(data, idx+skip)
            self.children.append(child)
            skip += eaten
        self.metadata = data[idx+skip:idx+skip+num_metadata]
        skip += num_metadata

        return self, skip


def read_input(path):
    with open(path, "r") as f:
        data = tuple(map(int, f.read().strip().split()))

    root, count = Node.load(data)
    return root


def part1(args):
    root = read_input(args.input)
    total = 0

    def sum_meta(node):
        nonlocal total
        total += sum(node.metadata)

    root.walk(sum_meta)
    print("{} meta_sum".format(total))


def part2(args):
    root = read_input(args.input)
    print("root val: {}".format(root.value))
    idx = 0

    def print_node(node):
        nonlocal idx
        print("{}: {} - {}".format(idx, node.value, node.metadata))
        idx += 1

    #root.walk(print_node)


if args.part2:
    part2(args)
else:
    part1(args)
