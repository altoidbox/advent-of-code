OP_ADD = 1
OP_MULT = 2
OP_HALT = 99


def read_file(path):
    with open(path, "r") as f:
        data = list(map(int, f.read().split(',')))
    return data


class HaltException(Exception):
    pass


class Machine(object):
    def __init__(self, program):
        self.program = list(program)
        self.opmap = {
            OP_ADD: self.add,
            OP_MULT: self.mult,
            OP_HALT: self.halt
        }

    def add(self, i):
        op, s1, s2, d = self.program[i:i+4]
        self.program[d] = self.program[s1] + self.program[s2]
        return 4

    def mult(self, i):
        op, s1, s2, d = self.program[i:i + 4]
        self.program[d] = self.program[s1] * self.program[s2]
        return 4

    def halt(self, i):
        raise HaltException()

    def run(self):
        i = 0
        try:
            while True:
                i += self.opmap[self.program[i]](i)
        except HaltException:
            return self.program[0]


def part1():
    data = read_file("input.txt")
    data[1] = 12
    data[2] = 2
    m = Machine(data)
    print("{}".format(m.run()))


def part2():
    result = 0
    data = read_file("input.txt")
    for noun in range(0, 100):
        for verb in range(0, 100):
            m = Machine(data)
            m.program[1] = noun
            m.program[2] = verb
            try:
                result = m.run()
            except:
                print("error", noun, verb)
                continue
            if result == 19690720:
                print("success", noun, verb)
                result = 100 * noun + verb
                print("{}".format(result))
                return


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
