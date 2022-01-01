import re
from collections import deque


def read_file(fname):
    progs = []
    with open(fname, 'r') as f:
        for lineno, line in enumerate(f):
            if lineno % 18 == 0:
                prog = []
                progs.append(prog)
            prog.append(line)
    return progs


class Processor(object):
    REGEXP = re.compile(r'(\w{3}) +([w-z]) ?([w-z]|-?\d+)?')
    REGS = {'w', 'x', 'y', 'z'}

    def __init__(self, input_='', state=None):
        if state:
            self.state = dict(state)
        else:
            self.state = {reg: 0 for reg in self.REGS}
        self.input = deque(input_)
        self.debug = False
    
    def __getitem__(self, key):
        return self.state[key]

    def getstate(self):
        return dict(self.state)

    def reset(self):
        self.state = {reg: 0 for reg in self.REGS}

    def getval(self, name_or_val):
        if name_or_val in self.state:
            return self.state[name_or_val]
        elif name_or_val is None:
            return None
        return int(name_or_val)
    
    def inp(self, a, b=None):
        self.state[a] = int(self.input.popleft())

    def add(self, a, b):
        self.state[a] += self.getval(b)

    def mul(self, a, b):
        self.state[a] *= self.getval(b)

    def div(self, a, b):
        self.state[a] //= self.getval(b)

    def mod(self, a, b):
        self.state[a] %= self.getval(b)

    def eql(self, a, b):
        self.state[a] = int(self.state[a] == self.getval(b))

    def decode(self, line):
        m = self.REGEXP.match(line)
        if self.debug:
            print(m.groups())
        return m.group(1), m.group(2), m.group(3)

    def run(self, prog, input_=None, state=None):
        if state:
            self.state = dict(state)
        if input_:
            self.input = deque(input_)
        for line in prog:
            if not line.strip():
                continue
            op, a, b = self.decode(line)
            getattr(self, op)(a, b)
            if self.debug:
                print(self.state)


def filter_states(outputs):
    for z, inputs in outputs.items():
        outputs[z] = max(inputs)
    return outputs


class RecursiveRunner(object):
    def __init__(self, proc, progs):
        self.proc = proc
        self.progs = progs
        self.end_idx = None
        self.outputs = {}
        self.reverse = False

    def run(self, prog_idx, init_state, inputs):
        values = range(1, 10)
        if self.reverse:
            values = reversed(values)
        for i in values:
            inputs.append(i)
            self.proc.run(self.progs[prog_idx], str(i), init_state)
            if prog_idx != self.end_idx:
                self.run(prog_idx + 1, self.proc.getstate(), inputs)
            elif self.proc.state['x'] == 0:
                # x is the condition that determines whether or not to increase z
                self.outputs.setdefault(self.proc.state['z'], tuple(inputs))
            #if inputs == [9, 9, 2, 9]:
            #    print(inputs, self.proc.state)
            #    exit()

            inputs.pop()
    
    def run_outputs(self, start_idx, end_idx, outputs):
        self.outputs = {}
        self.end_idx = end_idx
        self.proc.reset()
        init_state = self.proc.getstate()
        for zval, inputs in outputs.items():
            init_state['z'] = zval
            self.run(start_idx, init_state, list(inputs))
        return self.outputs


def is_inflection(prog):
    op, a, b = Processor().decode(prog[4])
    assert(op == 'div')
    assert(a == 'z')
    return b != '1'


def find_solution(largest=True):
    progs = read_file('input.txt')
    p = Processor()
    rr = RecursiveRunner(p, progs)
    rr.reverse = largest
    inflection_pairs = []
    start = 0
    for i, prog in enumerate(progs):
        if is_inflection(prog):
            inflection_pairs.append((start, i))
            start = i + 1
    #print(inflection_pairs)
    outputs = {0: []}
    for start, end in inflection_pairs:
        outputs = rr.run_outputs(start, end, outputs)
    #filter_states(rr.outputs)
    print(''.join(str(d) for d in outputs[0]))


if __name__ == "__main__":
    #find_solution()
    find_solution(False)
