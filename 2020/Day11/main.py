

def read_file(path):
    with open(path, "r") as f:
        data = list(map(lambda s: s.strip(), f))
    return data


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

    @staticmethod
    def adjacent_slopes():
        for slope in Point.range(Point(-1, -1), Point(1, 1)):
            if slope.x == 0 and slope.y == 0:
                continue
            yield slope

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


class Grid(object):
    ADJACENT_DIRS = [p for p in Point.range(Point(-1, -1), Point(1, 1)) if not (p.x == 0 and p.y == 0)]
    PREV_DIRS = ADJACENT_DIRS[:4]
    NEXT_DIRS = ADJACENT_DIRS[4:]

    def __init__(self, values):
        self.values = []
        for row in values:
            self.values.append(list(row))
        self.height = 0
        self.width = 0
        self._init_sizes()

    def _init_sizes(self):
        self.height = len(self.values)
        self.width = len(self.values[0]) if self.values else 0

    @staticmethod
    def create(width, height, init_val):
        grid = Grid([])
        row = [init_val] * width
        for _ in range(height):
            grid.values.append(list(row))
        grid.height = height
        grid.width = width
        return grid

    def dup(self):
        dup = Grid([])
        for row in self.values:
            dup.values.append(list(row))
        dup._init_sizes()
        return dup

    def each_point(self):
        for p in Point.range(Point(0, 0), Point(self.width - 1, self.height - 1)):
            yield p

    def items(self):
        for p in Point.range(Point(0, 0), Point(self.width - 1, self.height - 1)):
            yield p, self[p]

    def get(self, point, default=None):
        try:
            return self[point]
        except IndexError:
            return default

    def __getitem__(self, point):
        try:
            return self.values[point.y][point.x]
        except IndexError:
            raise IndexError("{} out of range for {} by {}".format(point, self.width, self.height))

    def __setitem__(self, point, value):
        self.values[point.y][point.x] = value

    def __contains__(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def __eq__(self, other):
        return self.values == other.values

    def __str__(self):
        return '\n'.join(''.join(str(v) for v in row) for row in self.values)

    def range(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                yield Point(x, y)

    def adjacent(self, point):
        lower_point = Point(max(0, point.x - 1), max(0, point.y - 1))
        upper_point = Point(min(self.width - 1, point.x + 1), min(self.height - 1, point.y + 1))
        for p in Point.range(lower_point, upper_point):
            if p.x == point.x and p.y == point.y:
                continue
            yield p


def count_adjacent(grid, point):
    count = 0
    for adj in grid.adjacent(point):
        if grid[adj] == '#':
            count += 1
    return count


def print_adj(grid):
    new_grid = grid.dup()
    for point, value in grid.items():
        if value == '#':
            new_grid[point] = str(count_adjacent(grid, point))
    print(new_grid)


def move(grid):
    num_moves = 0
    new_grid = grid.dup()
    for point, value in grid.items():
        if value == '.':
            # Nothing happens
            continue
        num_adj = count_adjacent(grid, point)
        if value == 'L' and num_adj == 0:
            new_grid[point] = '#'
            num_moves += 1
        elif value == '#' and num_adj >= 4:
            new_grid[point] = 'L'
            num_moves += 1
    return num_moves, new_grid


def part1(path):
    grid = Grid(read_file(path))
    num_moves = 1
    while num_moves:
        num_moves, grid = move(grid)
    print(len(list(v for p, v in grid.items() if v == '#')))


def look(grid, point, slope):
    while (point := point + slope) in grid:
        cur = grid[point]
        if cur != '.':
            return cur
    return '.'


def count_adjacent2(grid, point):
    count = 0
    for adj in Point.adjacent_slopes():
        if look(grid, point, adj) == '#':
            count += 1
    return count


def print_adj2(grid):
    new_grid = grid.dup()
    for point, value in grid.items():
        if value == '#':
            new_grid[point] = str(count_adjacent2(grid, point))
    print(new_grid)


def move2(grid):
    num_moves = 0
    new_grid = grid.dup()
    for point, value in grid.items():
        if value == '.':
            # Nothing happens
            continue
        num_adj = count_adjacent2(grid, point)
        if value == 'L' and num_adj == 0:
            new_grid[point] = '#'
            num_moves += 1
        elif value == '#' and num_adj >= 5:
            new_grid[point] = 'L'
            num_moves += 1
    return num_moves, new_grid


def part2(path):
    grid = Grid(read_file(path))
    num_moves = 1
    while num_moves:
        num_moves, grid = move2(grid)
    print(len(list(v for p, v in grid.items() if v == '#')))


def main():
    part1("example.txt")
    part1("input.txt")
    part2("example.txt")
    part2("input.txt")


if __name__ == "__main__":
    main()
