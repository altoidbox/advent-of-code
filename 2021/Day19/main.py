import sys
import functools
import math

def read_file(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('--'):
                cur = []
                data.append(cur)
                continue
            cur.append(Point(*[int(x) for x in line.split(',')]))
    return data


@functools.total_ordering
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

    def rotate(self, x, y, z):
        p = Point(*self.dims)
        for _ in range(x):
            tz = p.y
            p.y = -p.z
            p.z = tz
        for _ in range(y):
            tx = p.z
            p.z = -p.x
            p.x = tx
        for _ in range(z):
            ty = p.x
            p.x = -p.y
            p.y = ty
        return p

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
    
    def __mul__(self, other):
        return Point(*(s * o for s, o in zip(self.dims, other.dims)))

    def __eq__(self, other):
        return self.tuple == other.tuple

    def __lt__(self, other):
        return self.tuple < other.tuple

    def __str__(self):
        return "({})".format(",".join(str(d) for d in self.dims))

    def __repr__(self):
        return "Point({})".format(",".join(str(d) for d in self.dims))

    @staticmethod
    def range(a, b):
        xstep = 0
        ystep = 0
        if a.x < b.x:
            xstep = 1
        elif a.x > b.x:
            xstep = -1
        if a.y < b.y:
            ystep = 1
        elif a.y > b.y:
            ystep = -1
        p = Point(a.x, a.y)
        step = Point(xstep, ystep)
        while p.x != b.x or p.y != b.y:
            yield p
            p += step
        yield b


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


def make_rel_map(data_set):
    maps = {}
    for p in data_set:
        maps[p] = set()
        for p2 in data_set:
            maps[p].add(tuple(sorted(abs(v) for v in (p2-p).tuple)))
    return maps


def part1(fname):
    data = read_file(fname)
    map0 = make_rel_map(data[0])
    map1 = make_rel_map(data[1])
    for p in data[0]:
        for p2 in data[1]:
            similarity = map0[p].intersection(map1[p2])
            if len(map0[p].intersection(map1[p2])) >= 12:
                print(p, p2, len(similarity))
    print(sorted(map0[Point(-618,-824,-621)]))
    print(sorted(map1[Point(686,422,578)]))

def part2(fname):
    data = read_file(fname)


def main():
    fname = sys.argv[1]
    part1(fname)
    #part2()


if __name__ == "__main__":
    main()
