import re

def read_file(path):
    with open(path, "r") as f:
        return list(f)


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(self.tuple)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)

    @staticmethod
    def range(a, b):
        """a must be before b in this implementation"""
        xstart = a.x
        xstop = b.x + 1
        for y in range(a.y, b.y + 1):
            for x in range(xstart, xstop):
                yield Point(x, y)

    @property
    def tuple(self):
        return self.x, self.y

    def up(self, n):
        return Point(self.x, self.y - n)

    def down(self, n):
        return Point(self.x, self.y + n)

    def left(self, n):
        return Point(self.x - n, self.y)

    def forward(self, n):
        return Point(self.x + n, self.y)

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


class Aimed(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.aim = 0

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)

    @property
    def tuple(self):
        return self.x, self.y

    def up(self, n):
        self.aim -= n
        return self

    def down(self, n):
        self.aim += n
        return self

    def forward(self, n):
        self.x += n
        self.y += n * self.aim
        return self


def part1():
    cur = Point(0, 0)
    for line in read_file("input.txt"):
        m = re.match(r'(\w+) (\d+)', line)
        if not m:
            break
        cur = getattr(cur, m.group(1))(int(m.group(2)))
        #print(cur)
    print(cur.x * cur.y)


def part1():
    cur = Aimed(0, 0)
    for line in read_file("input.txt"):
        m = re.match(r'(\w+) (\d+)', line)
        if not m:
            break
        cur = getattr(cur, m.group(1))(int(m.group(2)))
        #print(cur)
    print(cur.x * cur.y)


def main():
    part1()


if __name__ == "__main__":
    main()
