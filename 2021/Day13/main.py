import sys


def read_file(path):
    g = Grid()
    with open(path, "r") as f:
        for line in f:
            if not line.strip():
                break
            x, y = tuple(int(x) for x in line.split(','))
            g[Point(x, y)] = '#'
        folds = [line.strip().split()[-1].split('=') for line in f]

    return g, folds


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
        ystart = min(a.y, b.y)
        ystop = max(a.y, b.y) + 1
        for x in range(min(a.x, b.x), max(a.x, b.x) + 1):
            for y in range(ystart, ystop):
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

    def right(self, n):
        return Point(self.x + n, self.y)

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


def minmax(it, key=lambda x: x):
    min_ = max_ = None
    for item in it:
        val = key(item)
        if min_ is None or val < min_:
            min_ = val
        if max_ is None or val > max_:
            max_ = val
    return min_, max_


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

    def fold(self, axis, value):
        #axis_max = getattr(self, 'max' + axis)
        moved_points = []
        for point in self:
            pval = getattr(point, axis)
            if pval < value:
                continue
            moved_points.append(point)
        for point in moved_points:
            self.pop(point)
            pval = getattr(point, axis)
            new_point = Point(point.x, point.y)
            setattr(new_point, axis, value - (pval - value))
            #print(point,'->', new_point, value, pval)
            self[new_point] = '#'

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
                line += str(self.get(Point(x, y), '.'))
            lines.append(line)
        return "\n".join(lines)


def part1(fname):
    g, folds = read_file(fname)
    for axis, value in folds:
        g.fold(axis, int(value))
        print(len(g))
        break


def part2(fname):
    g, folds = read_file(fname)
    for axis, value in folds:
        g.fold(axis, int(value))
    print(g)


def main():
    #part1(sys.argv[1])
    part2(sys.argv[1])


if __name__ == "__main__":
    main()
