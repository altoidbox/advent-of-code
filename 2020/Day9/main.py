import argparse
from bisect import bisect_left
import itertools
from collections import defaultdict, deque


def read_file(path):
    with open(path, "r") as f:
        return list(map(int, f))


class Xmas(object):
    def __init__(self):
        self.history = deque()
        self.values = defaultdict(lambda: 0)

    def load_preamble(self, values):
        self.history.extend(values)
        for pair in itertools.combinations(values, 2):
            if pair[0] == pair[1]:
                continue
            self.values[sum(pair)] += 1

    def next(self, value):
        if self.values[value] == 0:
            return False
        # now, we need to drop the first in history and add the current one
        removed = self.history.popleft()
        for v in self.history:
            if removed != v:
                self.values[removed + v] -= 1
            if value != v:
                self.values[value + v] += 1
        self.history.append(value)
        return True


def part1(data, preamle_len):
    x = Xmas()
    x.load_preamble(data[:preamle_len])
    for v in data[preamle_len:]:
        if not x.next(v):
            print(v)
            return v
    print("Not found")
    return None


def part2(data, value):
    total = data[0]
    li = ui = 0
    while total != value or li == ui:
        if total < value:
            ui += 1
            total += data[ui]
        else:
            total -= data[li]
            li += 1
        #print(li, ui, total, sum(data[li:ui+1]), data[li:ui+1])
    rg = data[li:ui+1]
    min_ = min(rg)
    max_ = max(rg)
    print("{} + {} = {}".format(min_, max_, min_ + max_))


def main():
    ex_data = read_file("example.txt")
    part2(ex_data, part1(ex_data, 5))
    input_data = read_file("input.txt")
    part2(input_data, part1(input_data, 25))


if __name__ == "__main__":
    main()
