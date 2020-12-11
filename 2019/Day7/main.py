from collections import deque
from itertools import permutations
from queue import Queue


OP_ADD = 1
OP_MULT = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LESS_THAN = 7
OP_EQUALS = 8
OP_HALT = 99


def read_file(path):
    with open(path, "r") as f:
        data = list(map(int, f.read().split(',')))
    return data


class HaltException(Exception):
    pass


class OutputException(Exception):
    def __init__(self, value):
        self.value = value


class Instruction(object):
    def __init__(self, inputs, outputs, method):
        self.inputs = inputs
        self.outputs = outputs
        self.method = method


class Machine(object):
    def __init__(self, memory):
        self.ip = 0
        self.next_ip = 0
        self.memory = list(memory)
        self.cur_op_modes = []
        self.opmap = {
            OP_ADD: Instruction(2, 1, self.add),
            OP_MULT: Instruction(2, 1, self.mult),
            OP_INPUT: Instruction(0, 1, self.input),
            OP_OUTPUT: Instruction(1, 0, self.output),
            OP_JUMP_IF_TRUE: Instruction(2, 0, self.jump_if_true),
            OP_JUMP_IF_FALSE: Instruction(2, 0, self.jump_if_false),
            OP_LESS_THAN: Instruction(2, 1, self.less_than),
            OP_EQUALS: Instruction(2, 1, self.equals),
            OP_HALT: Instruction(0, 0, self.halt)
        }
        self.inputs = deque()
        self.output = None

    def load(self, address):
        return self.memory[address]

    def op_load(self, opidx):
        v = self.memory[self.ip + 1 + opidx]
        if len(self.cur_op_modes) <= opidx or self.cur_op_modes[opidx] == 0:
            # memory load mode
            return self.memory[v]
        elif self.cur_op_modes[opidx] == 1:
            # immediate mode
            return v
        else:
            raise Exception("Invalid operand mode!")

    def op_store(self, opidx, value):
        address = self.memory[self.ip + 1 + opidx]
        self.memory[address] = value

    def execute(self):
        op = self.load(self.ip)
        instruction = self.opmap[op % 100]
        mode = op // 100
        modes = []
        while mode != 0:
            modes.append(mode % 10)
            mode //= 10
        self.cur_op_modes = modes
        self.next_ip = self.ip + 1 + instruction.inputs + instruction.outputs
        instruction.method()

    def add(self):
        self.op_store(2, self.op_load(0) + self.op_load(1))

    def mult(self):
        self.op_store(2, self.op_load(0) * self.op_load(1))

    def input(self):
        value = self.inputs.popleft()
        self.op_store(0, value)

    def output(self):
        value = self.op_load(0)
        # print(value)
        self.output = value
        raise OutputException(value)

    def jump_if_true(self):
        if self.op_load(0) != 0:
            self.next_ip = self.op_load(1)

    def jump_if_false(self):
        if self.op_load(0) == 0:
            self.next_ip = self.op_load(1)

    def less_than(self):
        self.op_store(2, int(self.op_load(0) < self.op_load(1)))

    def equals(self):
        self.op_store(2, int(self.op_load(0) == self.op_load(1)))

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


def run_amplifiers(program, inputs):
    procs = []
    for i in inputs:
        procs.append(Machine(program))
        procs[-1].inputs.append(i)

    result = 0
    while result is not None:
        for proc in procs:
            if result is not None:
                proc.inputs.append(result)
            result = proc.run()
    return procs[-1].output


def part1():
    data = read_file("input.txt")
    best = []
    best_val = -1
    for p in permutations(range(5)):
        result = run_amplifiers(data, p)
        if result > best_val:
            best_val = result
            best = p

    print(",".join(str(i) for i in best), best_val)


def part2():
    data = read_file("input.txt")
    best = []
    best_val = -1
    for p in permutations(range(5, 10)):
        result = run_amplifiers(data, p)
        if result > best_val:
            best_val = result
            best = p

    print(",".join(str(i) for i in best), best_val)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
