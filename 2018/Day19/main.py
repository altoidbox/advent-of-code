import argparse
from datetime import datetime
import re
from collections import deque


class Machine(object):
    def __init__(self):
        self.regs = [0] * 6
        self.operations = [
            self.addr, self.addi,
            self.mulr, self.muli,
            self.banr, self.bani,
            self.borr, self.bori,
            self.setr, self.seti,
            self.gtir, self.gtri, self.gtrr,
            self.eqir, self.eqri, self.eqrr
        ]
        self.ip = 0
        self.ip_reg = 0
        self.program = []

    def load_registers(self, regs):
        self.regs = list(regs)

    def reg_str(self):
        return ', '.join("{}: {:12}".format(idx, val) for idx, val in enumerate(self.regs))

    def insn_str(self, ip=None):
        if ip is None:
            ip = self.ip
        return "{} {}".format(self.program[ip][0], " ".join(map(str, self.program[ip][1])))

    def state_str(self, ip=None):
        if ip is None:
            ip = self.ip
        return "{:2} {:12} {}".format(ip, self.insn_str(ip), self.reg_str())

    def run_program(self, steps=-1, quiet=True):
        count = 0
        if not quiet:
            print("{:5}: {:2} {:12} {}".format(count, "", "", self.reg_str()))
        while self.ip < len(self.program) and (steps == -1 or count < steps):
            count += 1
            self.regs[self.ip_reg] = self.ip
            ip = self.ip
            getattr(self, self.program[self.ip][0])(*self.program[self.ip][1])
            self.ip = self.regs[self.ip_reg] + 1
            if not quiet:
                print("{:5}: {}".format(count, self.state_str(ip)))

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
    data = data.split()
    insn = data[0]
    args = tuple(map(int, data[1:]))
    return insn, args


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


def load_program(input):
    instructions = []
    ip_reg = 0
    with open(input, 'r') as f:
        for line in f:
            if line.startswith("#ip"):
                ip_reg = int(line.split()[1])
            else:
                instructions.append(parse_instruction(line))
    return ip_reg, instructions


def part1(args):
    ip_reg, instructions = load_program(args.input)
    m = Machine()
    m.ip_reg = ip_reg
    m.program = instructions
    m.run_program()
    print("reg state = {}".format(m.regs))


def part2(args):
    ip_reg, instructions = load_program(args.input)
    m = Machine()
    m.ip_reg = ip_reg
    m.program = instructions
    m.regs[0] = 1
    m.run_program(steps=28)
    # 127 * 251 * 331 == 10551287
    m.regs[3] = 1
    m.regs[5] = 10551287
    m.run_program(steps=13)
    m.regs[3] = 127
    m.regs[5] = 83081
    m.run_program(steps=8)
    m.regs[3] = 251
    m.regs[5] = 42037
    m.run_program(steps=8)
    m.regs[3] = 331
    m.regs[5] = 31877
    m.run_program(steps=8)
    m.regs[3] = 31877
    m.regs[5] = 331
    m.run_program(steps=8)
    m.regs[3] = 42037
    m.regs[5] = 251
    m.run_program(steps=8)
    m.regs[3] = 83081
    m.regs[5] = 127
    m.run_program(steps=8)
    m.regs[3] = 10551287
    m.regs[5] = 1
    m.run_program(steps=8)
    m.regs[3] = 10551287
    m.regs[5] = 10551287
    m.run_program(steps=20)
    print("reg state = {}".format(m.regs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--part2", action="store_true")

    args = parser.parse_args()

    if args.part2:
        part2(args)
    else:
        part1(args)
