import argparse
from datetime import datetime
import re
from collections import deque


class Machine(object):
    def __init__(self):
        self.regs = [0] * 4
        self.operations = [
            self.addr, self.addi,
            self.mulr, self.muli,
            self.banr, self.bani,
            self.borr, self.bori,
            self.setr, self.seti,
            self.gtir, self.gtri, self.gtrr,
            self.eqir, self.eqri, self.eqrr
        ]

    def load_registers(self, regs):
        self.regs = list(regs)

    def addr(self, a, b, c):
        self.regs[c] = self.regs[a] + self.regs[b]

    def addi(self, a, b, c):
        self.regs[c] = self.regs[a] + b

    def mulr(self, a, b, c):
        self.regs[c] = self.regs[a] * self.regs[b]

    def muli(self, a, b, c):
        self.regs[c] = self.regs[a] * b

    def banr(self, a, b, c):
        self.regs[c] = self.regs[a] & self.regs[b]

    def bani(self, a, b, c):
        self.regs[c] = self.regs[a] & b

    def borr(self, a, b, c):
        self.regs[c] = self.regs[a] | self.regs[b]

    def bori(self, a, b, c):
        self.regs[c] = self.regs[a] | b

    def setr(self, a, b, c):
        self.regs[c] = self.regs[a]

    def seti(self, a, b, c):
        self.regs[c] = a

    def gtir(self, a, b, c):
        self.regs[c] = int(a > self.regs[b])

    def gtri(self, a, b, c):
        self.regs[c] = int(self.regs[a] > b)

    def gtrr(self, a, b, c):
        self.regs[c] = int(self.regs[a] > self.regs[b])

    def eqir(self, a, b, c):
        self.regs[c] = int(a == self.regs[b])

    def eqri(self, a, b, c):
        self.regs[c] = int(self.regs[a] == b)

    def eqrr(self, a, b, c):
        self.regs[c] = int(self.regs[a] == self.regs[b])


def parse_array(data):
    return eval(data, {}, {})


def parse_instruction(data):
    return tuple(map(int, data.split()))


def load_samples(input):
    samples = []
    with open(input, 'r') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            parts = line.split(' ', 1)
            if parts[0] == "Before:":
                samples.append([])
                samples[-1].append(parse_array(parts[1]))
                i += 1
                samples[-1].append(parse_instruction(lines[i]))
                i += 1
                parts = lines[i].split(' ', 1)
                samples[-1].append(parse_array(parts[1]))
            i += 1
    return samples


def load_opcodes(input):
    opcodes = []
    with open(input, 'r') as f:
        for line in f:
            opcodes.append(parse_instruction(line))
    return opcodes


def part1(args):
    tests = load_samples(args.input)
    m = Machine()
    triple_op = 0
    for test in tests:
        matches = 0
        for op in m.operations:
            m.load_registers(test[0])
            op(*test[1][1:])
            if m.regs == test[2]:
                matches += 1
                if matches == 3:
                    triple_op += 1
                    break
    print("{}/{} samples match 3 or more opcodes".format(triple_op, len(tests)))


def part2(args):
    samples = load_samples('samples.txt')
    program = load_opcodes('opcodes.txt')
    m = Machine()
    opcandidates = {}
    for input, instruction, output in samples:
        opcode = instruction[0]
        if opcode not in opcandidates:
            opcandidates[opcode] = set()
            add_candidates = True
        else:
            if len(opcandidates[opcode]) == 1:
                continue
            add_candidates = False
        for op in m.operations:
            m.load_registers(input)
            arguments = instruction[1:]
            op(*arguments)
            if add_candidates and m.regs == output:
                # print("{} may   be {}".format(opcode, op.__name__))
                opcandidates[opcode].add(op)
            elif not add_candidates and m.regs != output and op in opcandidates[opcode]:
                # print("{} can't be {}".format(opcode, op.__name__))
                opcandidates[opcode].remove(op)
    unique_funcs = deque()
    func_table = {}
    optable = {}
    for opcode in opcandidates.keys():
        for op in opcandidates[opcode]:
            func_table.setdefault(op, set()).add(opcode)
        if len(opcandidates[opcode]) != 1:
            # print("{} has other one matching function: {}".format(opcode, ', '.join(f.__name__ for f in opcandidates[opcode])))
            pass
        else:
            # print("{} == {}".format(opcode, opcandidates[opcode].__name__))
            op = opcandidates[opcode].pop()
            optable[opcode] = op
            unique_funcs.append(op)
    while len(unique_funcs):
        func = unique_funcs.popleft()
        for opcode in func_table[func]:
            if func in opcandidates[opcode]:
                opcandidates[opcode].remove(func)
                if len(opcandidates[opcode]) == 1:
                    op = opcandidates[opcode].pop()
                    optable[opcode] = op
                    unique_funcs.append(op)
    for op, func in optable.items():
        print("{}: {}".format(op, func.__name__))

    for instruction in program:
        optable[instruction[0]](*instruction[1:])

    print(m.regs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--part2", action="store_true")

    args = parser.parse_args()

    if args.part2:
        part2(args)
    else:
        part1(args)
