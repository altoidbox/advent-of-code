#!/usr/bin/env python3

import argparse


def load(path):
    with open(path, "r") as f:
        data = [int(line.strip()) for line in f]
    return data


def mix(secret, other):
    return secret ^ other


def prune(secret):
    return secret % 16777216


def mix_prune(secret, other):
    return (secret ^ other) % 16777216


def generate(secret):
    secret = mix_prune(secret, secret * 64)
    secret = mix_prune(secret, secret // 32)
    secret = mix_prune(secret, secret * 2048)
    return secret


def generate_n(secret, n):
    for _ in range(n):
        secret = generate(secret)
    return secret


def generate_prices(secret):
    sequences = {}
    changes = []
    price = secret % 10
    for _ in range(2000):
        secret = generate(secret)
        new_price = secret % 10
        changes.append(new_price - price)
        price = new_price
        if len(changes) < 4:
            continue
        key = tuple(changes[-4:])
        if key not in sequences:
            sequences[key] = new_price
    return sequences


def update_sums(sums, new):
    for k, v in new.items():
        sums[k] = sums.get(k, 0) + v


def part1(path):
    data = load(path)
    total = 0
    for secret in data:
        new = generate_n(secret, 2000)
        #print(f'{secret}: {new}')
        total += new
    print(total)


def part2(path):
    data = load(path)
    sums = {}
    for secret in data:
        update_sums(sums, generate_prices(secret))
    best = max(sums, key=sums.get)
    print(f'{best}: {sums[best]}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
