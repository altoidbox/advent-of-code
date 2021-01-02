import sys
import time
import msvcrt
from collections import deque


def getc():
    c = msvcrt.getch()
    if ord(c) == 3:
        raise KeyboardInterrupt()
    return c.decode()


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


def minmax(it, key=lambda x: x):
    min_ = max_ = None
    for item in it:
        val = key(item)
        if min_ is None or val < min_:
            min_ = val
        if max_ is None or val > max_:
            max_ = val
    return min_, max_


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

    def state(self):
        return list(self._memory)

    def load_state(self, state):
        self._memory = list(state)

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
        # print("*({}) = {}".format(address, value))

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


class Grid(dict):
    _sentinel = object()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._minx = self._maxx = 0
        self._miny = self._maxy = 0
        self._dirty = False

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._dirty = True

    def __setitem__(self, key, value):
        super(Grid, self).__setitem__(key, value)
        self._dirty = True
        return value

    def setdefault(self, key, default):
        result = self.get(key, self._sentinel)
        if result is self._sentinel:
            self[key] = default
            result = default
        return result

    def dim_size(self, dim):
        if len(self) == 0:
            return 0
        min_, max_ = minmax(self.keys(), key=lambda p: p[dim])
        return max_ - min_ + 1

    def _update_ranges(self):
        if self._dirty:
            self._minx, self._maxx = minmax(self.keys(), key=lambda p: p.x)
            self._miny, self._maxy = minmax(self.keys(), key=lambda p: p.y)
            self._dirty = False

    @property
    def minx(self):
        self._update_ranges()
        return self._minx

    @property
    def maxx(self):
        self._update_ranges()
        return self._maxx

    @property
    def miny(self):
        self._update_ranges()
        return self._miny

    @property
    def maxy(self):
        self._update_ranges()
        return self._maxy

    @property
    def width(self):
        return self.dim_size(0)

    @property
    def height(self):
        return self.dim_size(1)

    @property
    def depth(self):
        return self.dim_size(2)

    def __str__(self):
        lines = []
        for y in range(self.miny, self.maxy+1):
            line = ""
            for x in range(self.minx, self.maxx + 1):
                line += self.get(Point(x, y), ' ')
            lines.append(line)
        return "\n".join(lines)


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


DIRS = {
    1: Point(0, -1),
    2: Point(0, 1),
    3: Point(-1, 0),
    4: Point(1, 0),
}
DIR_KEYS = {'w': 1, 's': 2, 'a': 3, 'd': 4}


class Map(object):
    def __init__(self, program, auto=True):
        self.grid = Grid()
        self.distances = Grid()
        self.location = Point(0, 0)
        self.target_loc = None
        self.grid[self.location] = 'D'
        self.distances[self.location] = 0
        if auto:
            self.cpu = Machine(program, self.manual_input, self.handle_response)
        else:
            self.cpu = Machine(program, self.auto_explore_input, self.auto_explore_handle_response)
        # auto-explore specific
        self.visited = set(self.location)
        self.to_explore = deque()
        for i in range(1, 5):
            self.to_explore.append((self.location, i, self.cpu.state()))
        self.goal = None

    def manual_input(self):
        print(self.grid)
        # print(self.cpu.ip)
        answer = 0
        while answer < 1 or answer > 4:
            try:
                answer = DIR_KEYS[getc()]
            except KeyboardInterrupt:
                raise
            except:
                pass
        self.target_loc = self.location + DIRS[answer]
        return answer

    def auto_explore_input(self):
        if not self.to_explore:
            raise Exception("Done!")
        cur_loc, direction, state = self.to_explore.popleft()
        self.location = cur_loc
        self.target_loc = cur_loc + DIRS[direction]
        self.cpu.load_state(state)
        return direction

    def auto_explore_handle_response(self, response):
        distance = self.distances[self.location]
        if not self.handle_response(response):
            # hit a wall, nothing new to explore
            return
        # override the D
        self.grid[self.location] = '.'
        self.distances[self.location] = distance + 1
        for direction, n in dir_neighbors(self.location):
            if n in self.visited:
                continue
            self.visited.add(n)
            nval = self.grid.get(n, ' ')
            if nval == ' ':
                self.to_explore.append((self.location, direction, self.cpu.state()))

    def handle_response(self, response):
        if response == 0:
            self.grid[self.target_loc] = '#'
            return False
        if self.location == Point(0, 0):
            self.grid[self.location] = 'S'
        else:
            self.grid[self.location] = '.'
        self.location = self.target_loc
        if response == 1:
            self.grid[self.location] = 'D'
        elif response == 2:
            self.grid[self.location] = 'X'
            self.goal = self.location
        else:
            raise Exception("Unexpected response: {}".format(response))
        return True


def part1():
    data = read_file("input.txt")
    m = Map(data, False)
    try:
        m.cpu.run()
    except Exception:
        pass
    print(m.distances[m.goal], "shortest moves to goal")
    return m


def dir_neighbors(point):
    for v, d in DIRS.items():
        yield v, point + d


def neighbors(point):
    for d in DIRS.values():
        yield point + d


def read_grid(path):
    g = Grid()
    with open(path) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.rstrip()):
                p = Point(x, y)
                g[p] = c
    return g


def part2(grid_map):
    moves = deque()
    g = grid_map.grid
    moves.append((grid_map.goal, 0))
    visited = set()
    depth = 0
    cur = moves[0][0]
    visited.add(cur)
    while moves:
        cur, depth = moves.popleft()
        g[cur] = 'O'
        for n in neighbors(cur):
            if n in visited:
                continue
            visited.add(n)
            nval = g[n]
            if nval in '.SX':
                moves.append((n, depth + 1))
            elif nval != '#':
                print(visited)
                raise Exception("Unexpected at {}->{}: {}".format(cur, n, nval))
    print("{} minutes to fill all space".format(depth))


def main():
    grid_map = part1()
    part2(grid_map)


if __name__ == "__main__":
    main()
