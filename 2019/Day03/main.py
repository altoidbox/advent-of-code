FILE = "input.txt"
#FILE = "example1.txt"
#FILE = "example2.txt"


def read_file(path):
    with open(path, "r") as f:
        data = list(f)
    return list(line.split(",") for line in data)


class Diagram(object):
    def __init__(self):
        self.steps = 0
        self.cur = Point(0, 0)
        self.map = {}
        self._moves = {
            'U': self.up,
            'D': self.down,
            'L': self.left,
            "R": self.right
        }

    def move(self, c, n):
        self._moves[c](n)

    def insert(self, x, y):
        self.steps += 1
        self.map.setdefault((x, y), self.steps)

    def up(self, n):
        for y in range(self.cur.y - 1, self.cur.y - n - 1, -1):
            self.insert(self.cur.x, y)
        self.cur = self.cur.up(n)

    def down(self, n):
        for y in range(self.cur.y + 1, self.cur.y + n + 1):
            self.insert(self.cur.x, y)
        self.cur = self.cur.down(n)

    def left(self, n):
        for x in range(self.cur.x - 1, self.cur.x - n - 1, -1):
            self.insert(x, self.cur.y)
        self.cur = self.cur.left(n)

    def right(self, n):
        for x in range(self.cur.x + 1, self.cur.x + n + 1):
            self.insert(x, self.cur.y)
        self.cur = self.cur.right(n)


def manhatten_dist(t1, t2):
    return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tuple(self):
        return self.x, self.y

    def up(self, n):
        return Point(self.x, self.y - n)

    def down(self, n):
        return Point(self.x, self.y + n)

    def left(self, n):
        return Point(self.x - n, self.y)

    def right(self, n):
        return Point(self.x + n, self.y)

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


def part1():
    data = read_file(FILE)
    wires = []
    for wire in data:
        d = Diagram()
        for path in wire:
            direction = path[0]
            dist = int(path[1:])
            d.move(direction, dist)
        wires.append(d)
    intersections = set()
    for point in wires[0].map.keys():
        if point in wires[1].map:
            intersections.add(point)
            print(point)
    closest = min((manhatten_dist((0, 0), i) for i in intersections))

    print("{}".format(closest))


def part2():
    data = read_file(FILE)
    wires = []
    for wire in data:
        d = Diagram()
        for path in wire:
            direction = path[0]
            dist = int(path[1:])
            d.move(direction, dist)
        wires.append(d)
    intersections = set()
    for point in wires[0].map.keys():
        if point in wires[1].map:
            intersections.add(point)
            print(point)
    closest = min(wires[0].map[i] + wires[1].map[i] for i in intersections)

    print("{}".format(closest))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
