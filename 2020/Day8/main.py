FILE = "input.txt"
#FILE = "example.txt"


def read_file(path):
    with open(path, "r") as f:
        data = []
        for line in map(lambda s: s.strip(), f):
            op, val = line.split()
            val = int(val)
            data.append((op, val))
    return data


class Machine(object):
    def __init__(self, memory):
        self.memory = list(memory)
        self.acc = 0
        self.ip = 0
        self.visited = set()

    def run(self):
        while True:
            if self.ip in self.visited:
                return False
            elif self.ip == len(self.memory):
                return True
            elif self.ip > len(self.memory):
                return False
            self.visited.add(self.ip)
            op, value = self.memory[self.ip]
            if op == 'acc':
                self.acc += value
                self.ip += 1
            elif op == 'nop':
                self.ip += 1
            elif op == 'jmp':
                self.ip += value


def part1():
    data = read_file(FILE)
    m = Machine(data)
    m.run()
    print(m.acc)


def part2():
    data = read_file(FILE)
    for i in range(len(data)):
        orig_op, val = data[i]
        if orig_op == 'nop':
            data[i] = ('jmp', val)
        elif orig_op == 'jmp':
            data[i] = ('nop', val)
        else:
            continue
        m = Machine(data)
        if m.run():
            print(m.acc)
            break
        data[i] = (orig_op, val)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
