import argparse
from datetime import datetime
import re

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class Node:
    def __init__(self, v, prev=None, next=None):
        self.value = v
        self.prev = prev
        self.next = next

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.next = self.prev = None


class LinkedList(Node):
    def __init__(self, iterable=''):
        super().__init__(None, self, self)
        for v in iterable:
            self.append(v)

    def __len__(self):
        count = 0
        cur = self.head
        while cur is not self:
            count += 1
            cur = cur.next
        return count

    @property
    def head(self):
        return self.next

    @property
    def tail(self):
        return self.prev

    @property
    def isempty(self):
        return self.next == self.prev == self

    def append(self, value):
        node = Node(value, prev=self.prev, next=self)
        self.prev.next = node
        self.prev = node


def read_input(path):
    with open(path, "r") as f:
        return f.read().strip()


def react_bytearray(data):
    new_data = bytearray()
    i = 0
    while i < len(data):
        if i < len(data) - 1:
            c = chr(data[i])
            c2 = chr(data[i+1])
            if (c.isupper() and c.lower() == c2) or (c.islower() and c.upper() == c2):
                i += 2
                # print("Cancelling {}{}".format(c, c2))
                continue
        new_data.append(data[i])
        i += 1
    return new_data


def react(data_list, kill_val=None):
    cur = data_list.head
    while cur is not data_list.prev and cur is not data_list:
        c = cur.value
        if c.lower() == kill_val:
            node = cur
            cur = node.prev
            node.remove()
            if cur is data_list:
                cur = cur.next
            continue
        c2 = cur.next.value
        if (c.isupper() and c.lower() == c2) or (c.islower() and c.upper() == c2):
            # print("Cancelling {}{}".format(c, c2))
            node = cur
            cur = node.prev
            node.next.remove()
            node.remove()
            if cur is data_list:
                cur = cur.next
            continue
        cur = cur.next

    return data_list


def part1(args):
    data = read_input(args.input)

    if 0:
        bdata = bytearray(data, 'utf-8')
        idx = 0
        start = datetime.now()
        while True:
            idx += 1
            # print("Pass {}".format(idx))
            new_data = react_bytearray(bdata)
            if len(new_data) == len(bdata):
                break
            bdata = new_data
        end = datetime.now()
        print("total reacted len {} ({})".format(len(bdata), end-start))

    if 1:
        ldata = LinkedList(data)
        start = datetime.now()
        react(ldata)
        end = datetime.now()
        print("total reacted len {} ({})".format(len(ldata), end-start))


def part2(args):
    data = read_input(args.input)
    best = 11754
    best_val = 0
    for c in range(ord('a'), ord('z') + 1):
        ldata = LinkedList(data)
        react(ldata, kill_val=chr(c))
        cur_len = len(ldata)
        if cur_len < best:
            best = cur_len
            best_val = chr(c)
    print("best {} by removing {}".format(best, best_val))


if args.part2:
    part2(args)
else:
    part1(args)
