import argparse
from datetime import datetime
import re
from collections import deque


class Machine(object):
    def __init__(self, ip_reg, program):
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
        self.ip_reg = ip_reg
        self.program = program

    def load_registers(self, regs):
        self.regs = list(regs)

    def reg_str(self):
        return ', '.join("{}: {:8X}".format(idx, val) for idx, val in enumerate(self.regs))

    def insn_str(self, ip=None):
        if ip is None:
            ip = self.ip
        return "{} {}".format(self.program[ip][0], " ".join(map(str, self.program[ip][1])))

    def state_str(self, ip=None):
        if ip is None:
            ip = self.ip
        return "{:2} {:20} {}".format(ip, self.insn_str(ip), self.reg_str())

    def run_program(self, steps=-1, quiet=True, bp=set()):
        count = 0
        if not quiet:
            print("{:5}: {:2} {:20} {}".format(count, "", "", self.reg_str()))
        while self.ip < len(self.program) and (steps == -1 or count < steps):
            count += 1
            self.regs[self.ip_reg] = self.ip
            ip = self.ip
            getattr(self, self.program[self.ip][0])(*self.program[self.ip][1])
            self.ip = self.regs[self.ip_reg] + 1
            if not quiet:
                print("{:5}: {}".format(count, self.state_str(ip)))
            if ip in bp:
                break

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


def re_implement(r1=0):
    r2 = r1 | 0x10000
    r1 = 0xA1D291
    while True:
        r1 += r2 & 0xFF
        r1 &= 0xFFFFFF
        r1 *= 0x1016B
        r1 &= 0xFFFFFF
        if r2 < 0x100:
            break
        r2 >>= 8
    return r1


def find_all_solutions():
    solutions = set()
    r1 = 0
    while True:
        prev = r1
        r1 = re_implement(r1)
        if r1 in solutions:
            break
        solutions.add(r1)
    print(len(solutions))
    print(prev)


def part1(args):
    ip_reg, instructions = load_program(args.input)
    m = Machine(ip_reg, instructions)
    m.run_program(quiet=False, bp={17, 28})
    m.regs[5] = (m.regs[2] >> 8) - 1
    m.run_program(quiet=False, bp={17, 28})
    m.regs[5] = (m.regs[2] >> 8) - 1
    m.run_program(quiet=False, bp={17, 28})
    print(re_implement(), m.regs[1])


def part2(args):
    find_all_solutions()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--part2", action="store_true")

    args = parser.parse_args()

    if args.part2:
        part2(args)
    else:
        part1(args)
