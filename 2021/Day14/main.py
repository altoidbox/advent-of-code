import sys
from collections import Counter


def read_file(path):
    with open(path, "r") as f:
        poly = f.readline().strip()
        conv = {}
        f.readline()
        for line in f:
            from_, to = line.strip().split(' -> ')
            conv[from_] = to
    return poly, conv


def minmax(it, key=lambda x: x):
    min_ = max_ = None
    for item in it:
        val = key(item)
        if min_ is None or val < min_:
            min_ = val
        if max_ is None or val > max_:
            max_ = val
    return min_, max_


def model(poly, conv, rounds):
    for rnd in range(rounds):
        newpoly = []
        for i in range(len(poly)):
            pair = poly[i:i+2]
            newpoly.append(pair[0])
            newpoly.append(conv.get(pair, ''))
        poly = ''.join(newpoly)
    return poly


def part1(fname):
    poly, conv = read_file(fname)
    counts = Counter(model(poly, conv, 10))
    least, most = minmax(counts.values())
    print(most, least, most - least)


def part2(fname):
    poly, conv = read_file(fname)
    pair_counts = {}
    for pair in conv:
        # could probably save off the polys for each of these to make the next part a lot quicker
        pair_counts[pair] = Counter(model(pair, conv, 20))
        print(pair, pair_counts[pair])
    
    poly20 = model(poly, conv, 20)
    #print(Counter(poly20))
    counts = Counter()
    for i in range(len(poly20) - 1):
        pair = poly20[i:i+2]
        counts.update(pair_counts[pair])
        counts[pair[1]] -= 1
    counts[poly[-1]] += 1
    print(counts)
    least, most = minmax(counts.values())
    print(most, least, most - least)


if __name__ == "__main__":
    part1(sys.argv[1])
    part2(sys.argv[1])
