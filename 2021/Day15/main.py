import sys
import heapq


def read_file(path):
    with open(path, "r") as f:
        return [[int(x) for x in s.strip()] for s in f]


class Grid(object):
    def __init__(self, values):
        self.values = []
        for row in values:
            self.values.append(list(row))

    @property
    def width(self):
        return len(self.values[0])

    @property
    def height(self):
        return len(self.values)

    def get(self, point, default=None):
        try:
            return self[point]
        except IndexError:
            return default

    def __str__(self):
        return '\n'.join(''.join(str(v) for v in row) for row in self.values)

    def __getitem__(self, point):
        if point.x < 0 or point.y < 0:
            raise IndexError('nope')
        return self.values[point.y][point.x]

    def __setitem__(self, point, value):
        if point.x < 0 or point.y < 0:
            raise IndexError('nope')
        self.values[point.y][point.x] = value

    def __contains__(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def range(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield Point(x, y)

    def adjacent(self, point):
        for p in point.neighbors():
            if p in self:
                yield p


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

    def __lt__(self, other):
        return self.y < other.y or self.y == other.y and self.x < other.x

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)

    @staticmethod
    def range(a, b):
        ystart = min(a.y, b.y)
        ystop = max(a.y, b.y) + 1
        for x in range(min(a.x, b.x), max(a.x, b.x) + 1):
            for y in range(ystart, ystop):
                yield Point(x, y)

    @property
    def tuple(self):
        return self.x, self.y
    
    def neighbors(self):
        yield self.right()
        yield self.down()
        yield self.left()
        yield self.up()

    def up(self, n=1):
        return Point(self.x, self.y - n)

    def down(self, n=1):
        return Point(self.x, self.y + n)

    def left(self, n=1):
        return Point(self.x - n, self.y)

    def right(self, n=1):
        return Point(self.x + n, self.y)

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


def dijkstra(g, start, end):
    visited = {
        start: (None, 0)
    }
    to_visit = [(g[p], start, p) for p in g.adjacent(start)]
    heapq.heapify(to_visit)
    for c, s, p in to_visit:
        visited[p] = None
    while True:
        path_cost, source, dest = heapq.heappop(to_visit)
        visited[dest] = (source, path_cost)
        for n in g.adjacent(dest):
            if n not in visited:
                visited[n] = None
                heapq.heappush(to_visit, (path_cost + g[n], dest, n))
        if dest == end:
            break
    print(visited[dest][1])


def part1(fname):
    g = Grid(read_file(fname))
    dijkstra(g, Point(0, 0), Point(g.width - 1, g.height - 1))


def part2(fname):
    g = Grid(read_file(fname))
    for y in range(g.height):
        row = g.values[y]
        orig_width = len(row)
        for i in range(4):
            for x in range(orig_width):
                row.append(((row[x] + i) % 9) + 1)
    orig_height = len(g.values)
    for i in range(4):
        for y in range(orig_height):
            row = []
            for v in g.values[y]:
                row.append(((v + i) % 9) + 1)
            g.values.append(row)
    dijkstra(g, Point(0, 0), Point(g.width - 1, g.height - 1))


if __name__ == "__main__":
    part1(sys.argv[1])
    part2(sys.argv[1])
