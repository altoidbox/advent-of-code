#!/usr/bin/env python3

from collections import deque
from itertools import permutations
import argparse


OP_ADV = 0  # rA = rA // math.pow(2, combo(opd))
OP_BXL = 1  # rB = rB ^ literal(opd)
OP_BST = 2  # rB = combo(opd) % 8
OP_JNZ = 3  # if rA != 0: ip = literal(opd)
OP_BXC = 4  # rB = rB ^ rC
OP_OUT = 5  # print(combo(opd) % 8)
OP_BDV = 6  # rB = rA // math.pow(2, combo(opd))
OP_CDV = 7  # rC = rA // math.pow(2, combo(opd))


def load(path):
    registers = []
    with open(path, "r") as f:
        for line in f:
            if line.startswith('Register '):
                registers.append(int(line.split()[-1]))
            if line.startswith('Program:'):
                program = [int(x) for x in line.split()[-1].split(',')]
    return registers, program


class HaltException(Exception):
    pass


class OutputException(Exception):
    def __init__(self, value):
        self.value = value


class Register(object):
    def __init__(self, index):
        self.index = index

    def get(self, machine):
        return machine.registers[self.index]

    def set(self, machine, value):
        machine.registers[self.index] = value


class Instruction(object):
    def __init__(self, name, output: Register, inputs, method):
        self.name = name
        self.inputs = inputs
        self.output = output
        self.method = method


class Machine(object):
    rA = Register(0)
    rB = Register(1)
    rC = Register(2)

    def __init__(self, registers, program):
        self.ip = 0
        self.next_ip = 0
        self.registers = registers
        self.program = program
        self.outputs = []
        self.opmap = {
            OP_ADV: Instruction("ADV", self.rA, [self.rA, self.combo], self.div2pow),
            OP_BXL: Instruction("BXL", self.rB, [self.rB, self.literal], self.xor),
            OP_BST: Instruction("BST", self.rB, [self.combo], self.mod8),
            OP_JNZ: Instruction("JNZ", None, [self.rA, self.literal], self.jnz),
            OP_BXC: Instruction("BXC", self.rB, [self.rB, self.rC], self.xor),
            OP_OUT: Instruction("OUT", None, [self.combo], self.output),
            OP_BDV: Instruction("BDV", self.rB, [self.rA, self.combo], self.div2pow),
            OP_CDV: Instruction("CDV", self.rC, [self.rA, self.combo], self.div2pow),
        }

    def reset(self, regA, regB=0, regC=0):
        self.ip = 0
        self.next_ip = 0
        self.registers = [regA, regB, regC]
        self.outputs = []

    def literal(self, value):
        return value

    def combo(self, value):
        if 0 <= value <= 3:
            return value
        if 4 <= value < 7:
            return self.registers[value - 4]
        raise Exception("Invalid combo value")

    def execute(self):
        if self.ip + 1 >= len(self.program):
            raise HaltException()
        op = self.program[self.ip]
        operand = self.program[self.ip + 1]
        self.next_ip = self.ip + 2
        instruction = self.opmap[op]
        inputs = []
        for input_ in instruction.inputs:
            if isinstance(input_, Register):
                inputs.append(input_.get(self))
            else:
                inputs.append(input_(operand))
        # print(op, instruction.method.__name__, inputs)
        result = instruction.method(*inputs)
        if result is not None:
            instruction.output.set(self, result)

    def div2pow(self, num, denom):
        return num // (2 ** denom)

    def xor(self, a, b):
        return a ^ b
    
    def mod8(self, a):
        return a % 8
    
    def jnz(self, condition, location):
        if condition != 0:
            self.next_ip = location
        return None

    def output(self, opd):
        self.outputs.append(self.mod8(opd))
        return None

    def halt(self):
        raise HaltException()

    def run(self):
        try:
            while True:
                self.ip = self.next_ip
                self.execute()
        except OutputException as oe:
            return oe.value
        except HaltException:
            return None

    def run_one(self):
        num_outputs = len(self.outputs)
        try:
            while len(self.outputs) == num_outputs:
                self.ip = self.next_ip
                self.execute()
        except OutputException as oe:
            return oe.value
        except HaltException:
            return None

    def decode_operand(self, optype, opval):
        if optype == self.literal:
            return str(opval)
        if optype == self.combo:
            if 0 <= opval <= 3:
                return str(opval)  # + ' (combo)'
            if 4 <= opval < 7:
                return f'r{chr(ord("A") + opval - 4)}'  # (combo)'
        if optype == self.rA:
            return "rA"
        if optype == self.rB:
            return "rB"
        if optype == self.rC:
            return "rC"
        return '??'

    def print(self):
        print(self.registers)
        print(self.program)
        for i in range(0, len(self.program), 2):
            insn = self.opmap[self.program[i]]
            operand = self.program[i + 1]
            print(insn.name, operand, end=' ')
            print(self.decode_operand(insn.output, None), end=' = ')
            print(self.decode_operand(insn.inputs[0], operand), end=' ')
            print(insn.method.__name__, end=' ')
            if len(insn.inputs) > 1:
                print(self.decode_operand(insn.inputs[1], operand), end=' ')
            print()


def part1(path):
    regs, prog = load(path)
    machine = Machine(regs, prog)
    print(machine.registers)
    print(machine.program)
    machine.run()
    print(",".join(str(o) for o in machine.outputs))


"""
Solve so the the outputs == the program
[2, 4, 1, 1, 7, 5, 1, 5, 0, 3, 4, 4, 5, 5, 3, 0]

BST 4 | rB = rA mod8 
BXL 1 | rB = rB xor 1 
CDV 5 | rC = rA div rB 
BXL 5 | rB = rB xor 5 
ADV 3 | rA = rA div 3 
BXC 4 | rB = rB xor rC 
OUT 5 | ?? = rB output 
JNZ 0 | ?? = rA jnz 0 

while rA != 0:
    rB = (rA % 8) ^ 1
    rC = rA // 2**rB
    rB = rB ^ 5
    rA = rA // 2**3
    rB = rB ^ rC
    print(rB % 8)
"""

def solve_one(machine, goal, end_a):
    solutions = []
    for rA in range(end_a * (2**3), end_a * (2**3) + 2**3):
        machine.reset(rA)
        machine.run_one()
        if machine.outputs[0] == goal:
            solutions.append(rA)
    return solutions


def part2(path):
    regs, prog = load(path)
    machine = Machine(regs, prog)
    machine.print()

    prev_a = [0]
    for i in range(len(prog), 0, -1):
        next_a = []
        goal = prog[i-1]
        for ra in prev_a:
            next_a.extend(solve_one(machine, goal, ra))
        prev_a = set(next_a)
        #print(f'{i}: {goal}: {next_a}')
    new_a = min(prev_a)
    machine.reset(new_a)
    machine.run()
    print(machine.outputs)
    print(new_a)
    #print(machine.program)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
