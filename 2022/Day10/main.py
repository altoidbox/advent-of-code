#!/usr/bin/env python3
import argparse
import re
import math

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def load(path):
    data = []
    with open(args.input, "r") as f:
        for line in f:
            data.append(line.strip())
    return data


class CPU(object):
    def __init__(self):
        self.cycle = 0
        self.x = 1
        self.breakpoint = None
        self.bmeth = None
        self.display = []
    
    def set_breakpoint(self, cycle, method):
        self.breakpoint = cycle
        self.bmeth = method

    def runcycle(self):
        self.cycle += 1
        if self.breakpoint == self.cycle:
            self.bmeth(self)
        if abs(self.x - len(self.display)) <= 1:
            self.display.append('#')
        else:
            self.display.append('.')
        if len(self.display) == 40:
            print(''.join(self.display))
            self.display = []

    def noop(self):
        self.runcycle()
    
    def addx(self, value):
        self.runcycle()
        self.runcycle()
        self.x += int(value)

    def exec(self, inst):
        parts = inst.split(' ')
        getattr(self, parts[0])(*parts[1:])


def part1(data):
    cpu = CPU()
    total = 0
    def callback(cpu_):
        nonlocal total
        strength = cpu.cycle * cpu.x
        #print(cpu.cycle, cpu.x, strength)
        total += strength
        cpu.set_breakpoint(cpu.cycle + 40, callback)
    cpu.set_breakpoint(20, callback)
    for line in data:
        cpu.exec(line)
    print(total)


def part2(data):
    cpu = CPU()
    for line in data:
        cpu.exec(line)
    

data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

