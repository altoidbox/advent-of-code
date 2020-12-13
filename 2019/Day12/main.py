import re
import itertools
import math


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
        return list(Point3D(*(map(int, re.match(r'^<x=(\S+), y=(\S+), z=(\S+)>$', line).groups()))) for line in f)


class Point3D(object):
    def __init__(self, *dims):
        self.dims = list(dims)

    @property
    def x(self):
        return self.dims[0]

    @property
    def y(self):
        return self.dims[1]

    @property
    def z(self):
        return self.dims[2]

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
        return Point3D(*(s + o for s, o in zip(self.dims, other.dims)))

    def __sub__(self, other):
        return Point3D(*(s - o for s, o in zip(self.dims, other.dims)))

    def __neg__(self):
        return Point3D(*(-d for d in self.dims))

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


class Moon(object):
    def __init__(self, pos):
        self.pos = pos
        self.vel = Point3D(0, 0, 0)

    def apply_gravity(self, other):
        change_vector = []
        for s, o in zip(self.pos.dims, other.pos.dims):
            if s < o:
                change_vector.append(1)
            elif s > o:
                change_vector.append(-1)
            else:
                change_vector.append(0)
        self.vel += Point3D(*change_vector)

    def apply_gravity_dim(self, other, i):
        if self.pos[i] < other.pos[i]:
            self.vel[i] += 1
        elif self.pos[i] > other.pos[i]:
            self.vel[i] -= 1

    def dim_info(self, i):
        return self.pos[i], self.vel[i]

    def move(self):
        self.pos += self.vel

    def move_dim(self, i):
        self.pos[i] += self.vel[i]

    def p_energy(self):
        return sum(abs(d) for d in self.pos.dims)

    def k_energy(self):
        return sum(abs(d) for d in self.vel.dims)

    def energy(self):
        return self.p_energy() * self.k_energy()

    def __str__(self):
        return "P:{}, V:{}".format(self.pos, self.vel)

    def __repr__(self):
        return "Moon(P:{}, V:{}, E: {})".format(self.pos, self.vel, self.energy())


def pass_time(data):
    for m1, m2 in itertools.combinations(data, 2):
        m1.apply_gravity(m2)
        m2.apply_gravity(m1)
    for moon in data:
        moon.move()


def total_energy(moons):
    return sum(m.energy() for m in moons)


def part1():
    data = [Moon(p) for p in read_file("input.txt")]
    for _ in range(1000):
        pass_time(data)
    print(total_energy(data))


def pass_time_dim(data, i):
    for m1, m2, in itertools.combinations(data, 2):
        m1.apply_gravity_dim(m2, i)
        m2.apply_gravity_dim(m1, i)
    for m in data:
        m.move_dim(i)


def part2():
    data = [Moon(p) for p in read_file("input.txt")]
    cycles = []
    # Each axis operates independently, so find a cycle for each
    for dim in range(3):
        states = set()
        cur_state = tuple(m.dim_info(dim) for m in data)
        while cur_state not in states:
            states.add(cur_state)
            pass_time_dim(data, dim)
            cur_state = tuple(m.dim_info(dim) for m in data)
            # print(dim, cur_state)
        cycles.append(len(states))
    print(cycles)
    # Once we have the cycle for each axis, find the least common multiple to determine when all the cycles coincide
    print(math.lcm(*cycles))


def main():
    # example_part1()
    part1()
    part2()


if __name__ == "__main__":
    main()
