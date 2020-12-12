FILE = "input.txt"
# FILE = "example1.txt"
# FILE = "example2.txt"


def read_file(path):
    with open(path, "r") as f:
        return list((line[0], int(line[1:])) for line in f)


class MapPart1(object):
    def __init__(self):
        self.steps = 0
        self.cur = Point(0, 0)
        self.dir = 0
        self._dirs = {
            0: self.east,
            90: self.south,
            180: self.west,
            270: self.north,
        }
        self._moves = {
            'N': self.north,
            'S': self.south,
            'E': self.east,
            'W': self.west,
            'L': self.left,
            'R': self.right,
            'F': self.forward
        }

    def right(self, n):
        self.dir += n
        self.dir %= 360

    def left(self, n):
        self.dir -= n
        self.dir %= 360
        if self.dir < 0:
            self.dir += 360

    def forward(self, n):
        self._dirs[self.dir](n)

    def move(self, c, n):
        self._moves[c](n)

    def north(self, n):
        self.cur = self.cur.north(n)

    def south(self, n):
        self.cur = self.cur.south(n)

    def east(self, n):
        self.cur = self.cur.east(n)

    def west(self, n):
        self.cur = self.cur.west(n)


class MapPart2(object):
    def __init__(self):
        self.steps = 0
        self.cur = Point(0, 0)
        self.waypoint = Point(10, -1)
        self.dir = 0
        self._dirs = {
            0: self.east,
            90: self.south,
            180: self.west,
            270: self.north,
        }
        self._moves = {
            'N': self.north,
            'S': self.south,
            'E': self.east,
            'W': self.west,
            'L': self.left,
            'R': self.right,
            'F': self.forward
        }

    def right(self, n):
        self.left(360 - n)

    def left(self, n):
        while n > 0:
            diff = self.waypoint - self.cur
            self.waypoint = Point(self.cur.x + diff.y, self.cur.y - diff.x)
            n -= 90

    def forward(self, n):
        d = self.waypoint - self.cur
        for _ in range(n):
            self.cur = self.waypoint
            self.waypoint += d

    def move(self, c, n):
        self._moves[c](n)
        #print(self.cur, self.waypoint - self.cur)

    def north(self, n):
        self.waypoint = self.waypoint.north(n)

    def south(self, n):
        self.waypoint = self.waypoint.south(n)

    def east(self, n):
        self.waypoint = self.waypoint.east(n)

    def west(self, n):
        self.waypoint = self.waypoint.west(n)


def manhatten_dist(t1, t2):
    return abs(t1.x - t2.x) + abs(t1.y - t2.y)


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tuple(self):
        return self.x, self.y

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

    def north(self, n):
        return Point(self.x, self.y - n)

    def south(self, n):
        return Point(self.x, self.y + n)

    def west(self, n):
        return Point(self.x - n, self.y)

    def east(self, n):
        return Point(self.x + n, self.y)

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


def part1():
    data = read_file(FILE)
    d = MapPart1()
    for direction, dist in data:
        d.move(direction, dist)

    print("{}: {}".format(d.cur, manhatten_dist(Point(0, 0), d.cur)))


def part2():
    data = read_file(FILE)
    d = MapPart2()
    for direction, dist in data:
        d.move(direction, dist)

    print("{}: {}".format(d.cur, manhatten_dist(Point(0, 0), d.cur)))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
