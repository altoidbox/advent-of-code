def read_file(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            start, end = line.split(' -> ')
            data.append((Point(*[int(x) for x in start.split(',')]), Point(*[int(x) for x in end.split(',')])))

    return data


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


def part1():
    data = read_file('input.txt')
    #print(data)
    g = Grid()
    for start, end in data:
        if start.x == end.x:
            #print('v', start, end)
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                p = Point(start.x, y)
                g[p] = g.get(p, 0) + 1
        elif start.y == end.y:
            #print('h', start, end)
            for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                p = Point(x, start.y)
                g[p] = g.get(p, 0) + 1
        else:
            #print('s', start, end)
            pass
    count = 0
    for p, v in g.items():
        if v >= 2:
            count += 1
    print(count)
    #print(g)


def part2():
    data = read_file('input.txt')
    #print(data)
    g = Grid()
    for start, end in data:
        #print(start, end)
        for p in Point.range(start, end):
            #print(p)
            g[p] = g.get(p, 0) + 1
    count = 0
    for p, v in g.items():
        if v >= 2:
            count += 1
    print(count)
    #print(g)


def main():
    #part1()
    part2()


if __name__ == "__main__":
    main()
