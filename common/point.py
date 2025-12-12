from functools import total_ordering
import math


@total_ordering
class Point(object):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __hash__(self):
        return hash(self.tuple)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        raise ValueError('Wrong type')

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)
    
    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)
    
    def __iter__(self):
        return iter(self.tuple) 

    @staticmethod
    def limits(a, b):
        miny, maxy = min(a.y, b.y), max(a.y, b.y) + 1
        minx, maxx = min(a.x, b.x), max(a.x, b.x) + 1
        return Point(minx, maxx), Point(miny, maxy)
    
    @staticmethod
    def range(a, b):
        (minx, maxx), (miny, maxy) = Point.limits(a, b)
        for y in range(miny, maxy):
            for x in range(minx, maxx):
                yield Point(x, y)

    @property
    def tuple(self):
        return self.x, self.y

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


@total_ordering
class Point3D(object):
    def __init__(self, *dims):
        self.dims = list(dims)
        self._tuple = None

    def copy(self):
        return Point3D(*self.dims)

    @property
    def x(self):
        return self.dims[0]

    @x.setter
    def x(self, value):
        self.dims[0] = value
        self._tuple = None

    @property
    def y(self):
        return self.dims[1]

    @y.setter
    def y(self, value):
        self.dims[1] = value
        self._tuple = None

    @property
    def z(self):
        return self.dims[2]

    @z.setter
    def z(self, value):
        self.dims[2] = value
        self._tuple = None

    @property
    def tuple(self):
        # returning it like this makes it sort naturally as a tuple
        if not self._tuple:
            self._tuple = tuple(reversed(self.dims))
        return self._tuple

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
    
    def __mul__(self, other):
        return Point3D(*(s * o for s, o in zip(self.dims, other.dims)))
    
    def __floordiv__(self, other):
        return Point3D(*(s // o for s, o in zip(self.dims, other.dims)))
    
    def __truediv__(self, other):
        return Point3D(*(s / o for s, o in zip(self.dims, other.dims)))

    def __eq__(self, other):
        return self.tuple == other.tuple

    def __lt__(self, other):
        return self.tuple < other.tuple

    def __str__(self):
        return "({})".format(",".join(str(d) for d in self.dims))

    def __repr__(self):
        return "Point3D({})".format(",".join(str(d) for d in self.dims))

    def adjacent(self, include_self=False):
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if 0 == x == y == z and not include_self:
                        continue
                    yield self + Point3D(x, y, z)

    def orthogonally_adjacent(self):
        for x in (-1, 1):
            yield self + Point3D(x, 0, 0)
        for y in (-1, 1):
            yield self + Point3D(0, y, 0)
        for z in (-1, 1):
            yield self + Point3D(0, 0, z)

    @staticmethod
    def range(start, end):
        for x in range(start.x, end.x + 1):
            for y in range(start.y, end.y + 1):
                for z in range(start.z, end.z + 1):
                    yield Point3D(x, y, z)

    def dist(self, other):
        return sum(abs(s - o) for s, o in zip(self.dims, other.dims))

    def euclidean_dist(self, other):
        return math.sqrt(sum((s - o) ** 2 for s, o in zip(self.dims, other.dims)))

    def rotate(self, x, y, z):
        p = Point(*self.dims)
        for _ in range(x % 4):
            tz = p.y
            p.y = -p.z
            p.z = tz
        for _ in range(y % 4):
            tx = p.z
            p.z = -p.x
            p.x = tx
        for _ in range(z % 4):
            ty = p.x
            p.x = -p.y
            p.y = ty
        return p
