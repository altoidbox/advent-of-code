import re
from collections import OrderedDict, defaultdict
import time


def read_file(path):
    with open(path, "r") as f:
        signal = list(map(int, f.readline().strip()))
        pattern = list(map(int, f.readline().split(',')))
    return signal, pattern


def fft_round_old(signal, pattern, round_num):
    total = 0
    pi = 0
    pc = 1
    rpt = round_num + 1
    dbg = ""
    si = 0
    pv = pattern[pi]

    if pv == 0:
        si += rpt - pc
        pi += 1
        pc = 0
        pv = pattern[pi]
    while si < len(signal):
        if pc == rpt:
            pi = (pi + 1) % len(pattern)
            pv = pattern[pi]
            pc = 0
            if pattern[pi] == 0:
                si += rpt
                pi = (pi + 1) % len(pattern)
                pv = pattern[pi]
                continue
        # dbg += "{}*{:-2d} + ".format(signal[si], pv)
        total += signal[si] * pv
        pc += 1
        si += 1
    ans = abs(total) % 10
    # print(dbg, ans)
    return ans


class State(object):
    # pattern is fixed
    PATTERN = [0, 1, 0, -1]

    def __init__(self, signal, pattern_repeat):
        self.signal = signal
        # how many times we repeat the pattern indexes
        self.pattern_repeat = pattern_repeat
        self.pattern_index = 0
        # Rules say we skip the very first pattern
        self.pattern_count = 1
        self.signal_index = 0
        self.wrap_if()
        self.skip()

    @property
    def pattern_value(self):
        return self.PATTERN[self.pattern_index]

    @property
    def signal_value(self):
        return self.signal[self.signal_index]

    def wrap_if(self):
        if self.pattern_count == self.pattern_repeat:
            self.wrap_pattern_index()

    def wrap_pattern_index(self):
        self.pattern_count = 0
        self.pattern_index += 1
        if self.pattern_index == len(self.PATTERN):
            self.pattern_index = 0

    def skip(self):
        if self.PATTERN[self.pattern_index] == 0:
            self.signal_index += self.pattern_repeat - self.pattern_count
            self.wrap_pattern_index()

    def increment(self):
        self.pattern_count += 1
        self.wrap_if()
        self.signal_index += 1

    def tuple(self):
        return self.signal_index, self.pattern_count, self.pattern_index

    def run_once(self):
        cur_total = 0
        while self.signal_index < len(self.signal):
            # dbg += "{}*{:-2d} + ".format(signal[si], pv)
            cur_total += self.signal_value * self.pattern_value
            self.increment()
        self.signal_index -= len(self.signal)
        return cur_total, self.tuple()

    def load(self, si, pc, pi):
        self.signal_index = si
        self.pattern_count = pc
        self.pattern_index = pi


def fft_round(signal, pattern, round_num, recycle):
    total = 0
    state = State(signal, round_num + 1)
    dbg = ""
    history = {}

    next_key = state.tuple()
    for _ in range(recycle):
        cur_key = next_key
        if cur_key in history:
            cur_total, next_key = history[cur_key]
            state.load(*next_key)
            total += cur_total
            continue
        cur_total, next_key = state.run_once()
        total += cur_total
        history[cur_key] = (cur_total, next_key)
    ans = abs(total) % 10
    # print(dbg, ans)
    return ans


PATTERN = [0, 1, 0, -1]


def fft_round_new(signal, round_num):
    ptn = PATTERN
    ptn_idx = 1
    sig_idx = round_num
    sig_end = len(signal)
    total = 0
    round_num += 1
    while sig_idx < sig_end:
        if ptn_idx == 4:
            ptn_idx = 0
        if ptn[ptn_idx] == 0:
            sig_idx += round_num
            ptn_idx += 1
            continue
        end_idx = min(sig_idx + round_num, sig_end)
        tmp_sum = 0
        while sig_idx < end_idx:
            tmp_sum += signal[sig_idx]
            sig_idx += 1
        total += ptn[ptn_idx] * tmp_sum
        ptn_idx += 1
    if total < 0:
        total = -total
    result = total % 10
    return result


def fft_round_simple(signal, round_num):
    sig_end = len(signal)
    total = 0
    round_num += 1
    try:
        for add_idx in range(round_num - 1, sig_end, 4 * round_num):
            for idx in range(add_idx, add_idx + round_num):
                total += signal[idx]
    except IndexError:
        pass
    try:
        for sub_idx in range(round_num - 1 + 2 * round_num, sig_end, 4 * round_num):
            for idx in range(sub_idx, sub_idx + round_num):
                total -= signal[idx]
    except IndexError:
        pass

    if total < 0:
        total = -total
    result = total % 10
    return result


def fft_round_simple2(signal, round_num):
    sig_end = len(signal)
    total = 0
    round_num += 1
    for add_idx in range(round_num - 1, sig_end, 4 * round_num):
        for idx in range(add_idx, min(add_idx + round_num, sig_end)):
            total += signal[idx]
    for sub_idx in range(round_num - 1 + 2 * round_num, sig_end, 4 * round_num):
        for idx in range(sub_idx, min(sub_idx + round_num, sig_end)):
            total -= signal[idx]

    if total < 0:
        total = -total
    result = total % 10
    return result


def fft_round_simple3(signal, round_num):
    sig_end = len(signal)
    total = 0
    round_num += 1
    try:
        add_idx = round_num - 1
        while add_idx < sig_end:
            idx = add_idx
            while idx < add_idx + round_num:
                total += signal[idx]
                idx += 1
            add_idx += 4 * round_num

    except IndexError:
        pass
    try:
        sub_idx = round_num - 1 + 2 * round_num
        while sub_idx < sig_end:
            idx = sub_idx
            while idx < sub_idx + round_num:
                total -= signal[idx]
                idx += 1
            sub_idx += 4 * round_num
    except IndexError:
        pass

    if total < 0:
        total = -total
    result = total % 10
    return result


def fft_phase(signal, f):
    new_signal = []
    for round_num in range(len(signal)):
        #new_signal.append(fft_round(signal, pattern, round_num, recycle))
        #new_signal.append(fft_round_simple(signal, round_num))
        new_signal.append(f(signal, round_num))
    return new_signal


def part1(path, count, f=fft_round_simple):
    signal, pattern = read_file(path)
    #print(signal, pattern)
    for i in range(count):
        signal = fft_phase(signal, f)
        #print(i + 1, signal)
    print("".join(map(str, signal[:8])))


def part2(path, count, f=fft_round_simple):
    signal, pattern = read_file(path)
    index = int("".join(map(str, signal[:7])))
    signal *= 10000
    print(len(signal), index)
    for i in range(count):
        signal = fft_phase(signal, f)
    print(index, "".join(map(str, signal[index:8])))


def main():
    part1('example1.txt', 4)
    part1('example2.txt', 100)
    part1('example3.txt', 100)
    part1('example4.txt', 100)
    s = time.time()
    part1('input.txt', 100, fft_round_simple)
    print("Took {}".format(time.time() - s))
    s = time.time()
    part1('input.txt', 100, fft_round_simple2)
    print("Took {}".format(time.time() - s))
    s = time.time()
    part1('input.txt', 100, fft_round_simple3)
    print("Took {}".format(time.time() - s))
    #s = time.time()
    #part2('example5.txt', 1)
    #print("Took {}".format(time.time() - s))
    #s = time.time()
    #part2('input.txt', 1)
    #print("Took {}".format(time.time() - s))
    # part2('input.txt')


if __name__ == "__main__":
    main()
