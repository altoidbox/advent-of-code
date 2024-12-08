#!/usr/bin/env python3
import argparse


def load(path):
    data = []
    with open(path) as f:
        for line in f:
            value, inputs = line.strip().split(':')
            data.append((int(value), [int(i) for i in inputs.split()]))
    return data


def add(l, r):
    return l + r


def mul(l, r):
    return l * r


def cat(l, r):
    return int(f'{l}{r}')


OPERATORS = {'+': add, '*': mul}
OPERATORS2 = {'+': add, '*': mul, '||': cat }


class RecursiveCominator(object):
    def __init__(self, target, inputs, operators):
        self.target = target
        self.inputs = inputs
        self.operators = operators

    def recursive_check(self, curval, idx):
        if curval > self.target:
            return False
        if idx == len(self.inputs):
            return curval == self.target
        for op in self.operators.values():
            if self.recursive_check(op(curval, self.inputs[idx]), idx+1):
                return True
        return False
    
    def run(self):
        return self.recursive_check(self.inputs[0], 1)


def part1(path):
    data = load(path)
    total = 0
    for value, inputs in data:
        if RecursiveCominator(value, inputs, OPERATORS).run():
            # print(value)
            total += value
    print(total)        


def part2(path):
    data = load(path)
    total = 0
    for value, inputs in data:
        if RecursiveCominator(value, inputs, OPERATORS2).run():
            # print(value)
            total += value
    print(total)  


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


main()
