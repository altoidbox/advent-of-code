import curses
import time


OP_ADD = 1
OP_MULT = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LESS_THAN = 7
OP_EQUALS = 8
OP_REL_BASE_OFFSET = 9
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
    def __init__(self, memory, f_input, f_output):
        self.ip = 0
        self.next_ip = 0
        self.rbo = 0
        self._memory = list(memory)
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
            OP_REL_BASE_OFFSET: Instruction(1, 0, self.adj_rel_base_offset),
            OP_HALT: Instruction(0, 0, self.halt)
        }
        self.f_input = f_input
        self.f_output = f_output

    def expand_mem(self, new_size):
        self._memory.extend((0 for _ in range(new_size - len(self._memory) + 1)))

    def load(self, address):
        try:
            return self._memory[address]
        except IndexError:
            self.expand_mem(address)
        return self._memory[address]

    def store(self, address, value):
        try:
            self._memory[address] = value
        except IndexError:
            self.expand_mem(address)
        self._memory[address] = value

    def op_load(self, opidx):
        v = self.load(self.ip + 1 + opidx)
        if len(self.cur_op_modes) <= opidx or self.cur_op_modes[opidx] == 0:
            # memory load mode
            return self.load(v)
        elif self.cur_op_modes[opidx] == 1:
            # immediate mode
            return v
        elif self.cur_op_modes[opidx] == 2:
            return self.load(self.rbo + v)
        else:
            raise Exception("Invalid operand mode!")

    def op_store(self, opidx, value):
        a = self.load(self.ip + 1 + opidx)
        if len(self.cur_op_modes) <= opidx or self.cur_op_modes[opidx] == 1:
            self.store(a, value)
        elif self.cur_op_modes[opidx] == 2:
            self.store(self.rbo + a, value)
        else:
            raise Exception("Invalid operand mode!")

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
        value = self.f_input()
        self.op_store(0, value)

    def output(self):
        value = self.op_load(0)
        self.f_output(value)

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

    def adj_rel_base_offset(self):
        self.rbo += self.op_load(0)

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


class Point(object):
    def __init__(self, *dims):
        self.dims = list(dims)

    def copy(self):
        return Point(*self.dims)

    @property
    def x(self):
        return self.dims[0]

    @x.setter
    def x(self, value):
        self.dims[0] = value

    @property
    def y(self):
        return self.dims[1]

    @y.setter
    def y(self, value):
        self.dims[1] = value

    @property
    def z(self):
        return self.dims[2]

    @z.setter
    def z(self, value):
        self.dims[2] = value

    @property
    def tuple(self):
        # returning it like this makes it sort naturally as a tuple
        return tuple(reversed(self.dims))

    def dist(self, other):
        return sum(s + o for s, o in zip(self.dims, other.dims))

    def __getitem__(self, item):
        return self.dims[item]

    def __setitem__(self, key, value):
        self.dims[key] = value

    def __hash__(self):
        return hash(self.tuple)

    def __add__(self, other):
        return Point(*(s + o for s, o in zip(self.dims, other.dims)))

    def __sub__(self, other):
        return Point(*(s - o for s, o in zip(self.dims, other.dims)))

    def __neg__(self):
        return Point(*(-d for d in self.dims))

    def __eq__(self, other):
        return all(s == o for s, o in zip(self.dims, other.dims))

    def __ne__(self, other):
        return any(s != o for s, o in zip(self.dims, other.dims))

    def __lt__(self, other):
        for s, o in zip(self.dims, other.dims):
            if s < o:
                return True
            elif s > o:
                return False
        return False

    def __le__(self, other):
        for s, o in zip(self.dims, other.dims):
            if s < o:
                return True
            elif s > o:
                return False
        return True

    def __gt__(self, other):
        for s, o in zip(self.dims, other.dims):
            if s > o:
                return True
            elif s < o:
                return False
        return False

    def __ge__(self, other):
        for s, o in zip(self.dims, other.dims):
            if s > o:
                return True
            elif s < o:
                return False
        return True

    def __str__(self):
        return "({})".format(",".join(str(d) for d in self.dims))

    def __repr__(self):
        return "Point({})".format(",".join(str(d) for d in self.dims))


TILE_EMPTY = 0
TILE_WALL = 1
TILE_BLOCK = 2
TILE_PADDLE = 3
TILE_BALL = 4
MODE_XPOS = 0
MODE_YPOS = 1
MODE_VAL = 2
MODE_LEN = 3
JOY_CENTER = 0
JOY_LEFT = -1
JOY_RIGHT = 1
SCORE_POS = Point(-1, 0)


class Console(object):
    SC_MAP = [' ', '+', '#', '-', '*']

    def __init__(self, program, stdscr=None, delay=0.0):
        self.stdscr = stdscr
        self.delay = delay
        self.screen = {}
        self.cpu = Machine(program, self.scan, self.instruct)
        self._mode = 0
        self._p_cur = Point(0, 0)
        self.score = 0
        self.b_pos = Point(0, 0)
        self.p_pos = Point(0, 0)

    def scan(self):
        self.show()
        time.sleep(self.delay)
        if self.p_pos.x == self.b_pos.x:
            return JOY_CENTER
        elif self.p_pos.x < self.b_pos.x:
            return JOY_RIGHT
        elif self.p_pos.x > self.b_pos.x:
            return JOY_LEFT
        return 0

    def instruct(self, value):
        if self._mode == MODE_XPOS:
            self._p_cur.x = value
        elif self._mode == MODE_YPOS:
            self._p_cur.y = value
        elif self._mode == MODE_VAL:
            if self._p_cur == SCORE_POS:
                self.score = value
                self.stdscr.addstr(0, 0, str(value).center(36))
            else:
                if value == TILE_BALL:
                    self.b_pos = self._p_cur.copy()
                if value == TILE_PADDLE:
                    self.p_pos = self._p_cur.copy()
                if self.stdscr:
                    self.stdscr.addch(self._p_cur.y + 1, self._p_cur.x, Console.SC_MAP[value])
                self.screen[self._p_cur.copy()] = value
        self._mode = (self._mode + 1) % MODE_LEN

    def show(self):
        if self.stdscr:
            self.stdscr.move(0, 0)
            self.stdscr.refresh()
        else:
            min_point = Point(min(p.x for p in self.screen), min(p.y for p in self.screen))
            max_point = Point(max(p.x for p in self.screen), max(p.y for p in self.screen))
            print(self.score)
            for y in range(min_point.y, max_point.y + 1):
                print(''.join(
                    Console.SC_MAP[self.screen.get(Point(x, y), 0)] for x in range(min_point.x, max_point.x + 1)))


def part1():
    data = read_file("input.txt")
    c = Console(data)
    c.cpu.run()
    print(len(list(filter(None, (v == 2 for v in c.screen.values())))))


def part2():
    stdscr = curses.initscr()
    try:
        height, width = stdscr.getmaxyx()
        if width < 36 or height < 23:
            curses.endwin()
            stdscr = None
        else:
            curses.curs_set(0)
        data = read_file("input.txt")
        data[0] = 2
        c = Console(data, stdscr, 0.002)
        c.cpu.run()
    finally:
        if stdscr:
            curses.endwin()
    print(c.score)


def main():
    # example_part1()
    part1()
    part2()


if __name__ == "__main__":
    main()
