#!/usr/bin/env python3

import argparse
import math


def readlines_stripped(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data


def load(path):
    data = ''.join(readlines_stripped(path))
    ranges = []
    for range_ in data.split(','):
        low, high = (int(x) for x in range_.split('-'))
        ranges.append(range(low, high+1))
    return ranges


def mkrepeat(num):
    numstr = str(num)
    return int(numstr + numstr)


def test_pairs1(rg):
    ids = []
    start = str(rg.start)
    #stop = str(rg.stop)
    if (len(start) & 1) != 0:
        pow = int(math.log(rg.start, 10))
        start = str(int(math.pow(10, pow + 1)))
    #if (len(stop) & 1) != 0:
    #    pow = int(math.log(rg.start, 10))
    #    stop = str(int(math.pow(10, pow)))
    half1 = int(start[:len(start)//2])
    while True:
        value = mkrepeat(half1)
        if value < rg.start:
            half1 += 1
            #print(f'{value}  < {rg}')
            continue
        elif value >= rg.stop:
            #print(f'{value}  > {rg}')
            break
        #print(f'{value} in {rg}')
        ids.append(value)
        half1 += 1
    return ids


def part1(path):
    ranges = load(path)
    total = 0
    for rg in ranges:
        total += sum(test_pairs1(rg))
    print(total)


def generate_sequences(min_len, max_len):
    done = set()
    # for every possible repeated sequence length
    for seq_len in range(1, 1 + max_len // 2):
        #print(f'seq_len={seq_len}')
        # calculate the minimum and maximum number of repetitions of this sequence
        # for the desired output length
        min_repeat = int(math.ceil(min_len / seq_len))
        max_repeat = int(math.floor(max_len / seq_len))
        # We must repeat the sequence at least twice (a single instance is not really a repetition)
        # Increasing the min is fine since it will still be validated against the max
        if min_repeat < 2:
            min_repeat = 2
        # if there are no possible repetitions for this sequence, skip it
        if min_repeat > max_repeat:
            continue
        # for each possible number of repetitions
        for repeat in range(min_repeat, 1 + max_repeat):
            #print(f'repeat={repeat}')
            # Since leading zeros are not allowed, start with the smallest number of the desired sequence length
            # We can calcualte it by using powers of 10
            min_val = int(math.pow(10, seq_len - 1))
            # and end with the largest number of the desired sequence length (exclusive)
            max_val = int(math.pow(10, seq_len))
            # calculate a multiplier that will result in the desired number of repetitions
            # e.g., 11 * a single digit number will repeat it twice, 111 will repeat it 3 times
            #       101 * a double digit number will repeat it twice, 10101 will repeat it 3 times
            #       1001 * a triple digit number will repeat it twice, 1001001 will repeat it 3 times
            # and so on and so forth for additional digit lengths and additional quantities of repetitions
            mult = 0
            for _ in range(repeat):
                mult *= max_val
                mult += 1
            #print(f'min_val={min_val},max_val={max_val},mult={mult}')
            for seq in range(min_val, max_val):
                value = seq * mult
                # we don't otherwise exclude duplicates, so maintain a set to determine if we've already produced it
                if value in done:
                    continue
                yield value
                done.add(value)


def test_pairs2(rg):
    ids = []
    for value in generate_sequences(len(str(rg.start)), len(str(rg.stop-1))):
        if value in rg:
            ids.append(value)
    return ids


def part2(path):
    ranges = load(path)
    total = 0
    for rg in ranges:
        total += sum(test_pairs2(rg))
    print(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
