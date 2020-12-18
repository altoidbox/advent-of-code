

def minmax(it, key=lambda x: x):
    min_ = max_ = None
    for item in it:
        val = key(item)
        if min_ is None or val < min_:
            min_ = val
        if max_ is None or val > max_:
            max_ = val
    return min_, max_


def minmax_item(*args, key=lambda x: x):
    if len(args) > 1:
        it = args
    else:
        it = args[0]
    minval = minitem = maxval = maxitem = None
    for item in it:
        val = key(item)
        if minval is None or val < minval:
            minval, minitem = val, item
        if maxval is None or val > maxval:
            maxval, maxitem = val, item
    return minitem, maxitem


def read_file(path, dims):
    g = Grid()
    with open(path, "r") as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    g[Point3D(x, y, *([0] * (dims - 2)))] = True
    return g


class Grid(dict):
    def dim_size(self, dim):
        if len(self) == 0:
            return 0
        min_, max_ = minmax(self.keys(), key=lambda p: p[dim])
        return max_ - min_ + 1

    @property
    def width(self):
        return self.dim_size(0)

    @property
    def height(self):
        return self.dim_size(1)

    @property
    def depth(self):
        return self.dim_size(2)


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

    def adjacent(self):
        count = len(self.dims)
        if count == 3:
            f = self.adjacent3
        elif count == 4:
            f = self.adjacent4
        else:
            raise Exception("Unsupported size: {}".format(count))
        for p in f():
            yield p

    def adjacent3(self):
        for x in range(-1, 1 + 1):
            for y in range(-1, 1 + 1):
                for z in range(-1, 1 + 1):
                    if 0 == x == y == z:
                        continue
                    yield self + Point3D(x, y, z)

    def adjacent4(self):
        for x in range(-1, 1 + 1):
            for y in range(-1, 1 + 1):
                for z in range(-1, 1 + 1):
                    for w in range(-1, 1 + 1):
                        if 0 == x == y == z == w:
                            continue
                        yield self + Point3D(x, y, z, w)

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


def execute_iteration(grid):
    adj_grid = Grid()
    new_grid = Grid()
    for point in grid:
        for adj in point.adjacent():
            adj_grid[adj] = adj_grid.get(adj, 0) + 1
    for point, value in adj_grid.items():
        if value == 3:
            new_grid[point] = True
        elif value == 2 and point in grid:
            new_grid[point] = True
    return new_grid


def part1():
    grid = read_file("input.txt", 3)
    for _ in range(6):
        grid = execute_iteration(grid)
    print(len(grid))


def part2():
    grid = read_file("input.txt", 4)
    for _ in range(6):
        grid = execute_iteration(grid)
    print(len(grid))


def main():
    # example_part1()
    part1()
    part2()


if __name__ == "__main__":
    main()
