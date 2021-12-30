import sys
import functools
from collections import Counter
from itertools import combinations


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
        return sum(abs(s - o) for s, o in zip(self.dims, other.dims))

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
    def range3(start, end):
        for x in range(start.x, end.x + 1):
            for y in range(start.y, end.y + 1):
                for z in range(start.z, end.z + 1):
                    yield Point(x, y, z)


class RelativePoint(object):
    def __init__(self, source, dest):
        self.source = source
        self.rel = dest - source
        self.abs_rel = tuple(sorted(abs(v) for v in self.rel.tuple))

    @property
    def dest(self):
        return self.rel + self.source

    def __str__(self):
        return 'RP{}->{}={}'.format(self.source, self.dest, self.rel)

    def __repr__(self):
        return str(self)


class RelativeMap(object):
    def __init__(self, source, points):
        self.source = source
        self.pmap = {}
        self.rmap = {}
        self.set = set()
        for p in points:
            if p == source:
                continue
            rel_point = RelativePoint(source, p)
            self.pmap[p] = rel_point
            self.rmap.setdefault(rel_point.abs_rel, []).append(rel_point)
            self.set.add(rel_point.abs_rel)

    def __str__(self):
        return 'RM{}'.format(self.source)

    def __repr__(self):
        return str(self)


def make_rel_map(data_set):
    maps = {}
    for p in data_set:
        maps[p] = RelativeMap(p, data_set)
    return maps


class ScannerMap(object):
    def __init__(self, points):
        self.points = points
        self._relmap = None
    
    @property
    def relmap(self):
        if not self._relmap:
            self._relmap = make_rel_map(self.points)
        return self._relmap

    def reorient(self, info):
        for i, p in enumerate(self.points):
            self.points[i] = reorient(p, info)
        self._relmap = None


def reorient(p, info):
    new_p = Point(0, 0, 0)
    for i, (sign, other_i) in enumerate(info):
        new_p.dims[other_i] = p.dims[i] * sign
    return new_p


def find_point_reorientation(rp0, rp1):
    """
    Create info to reorient rp1 (RelativePoint1) to rp0
    """
    if len(rp0) > 1:
        raise Exception('rp0 not unique!')
    if len(rp1) > 1:
        raise Exception('rp1 not unique!')
    if len(Counter(rp0[0].abs_rel)) != 3:
        raise Exception('orientation not unique!')
    r0 = rp0[0].rel
    r1 = rp1[0].rel
    abs_r0 = [abs(v) for v in r0.dims]
    abs_r1 = [abs(v) for v in r1.dims]
    info = []
    for i, v in enumerate(abs_r1):
        other_i = abs_r0.index(v)
        sign = 1 if r1[i] == r0[other_i] else -1
        info.append((sign, other_i))
    offset = rp0[0].source - reorient(rp1[0].source, info)
    return info, offset


def find_scanner_reorientation(s0, s1, similar):
    """
    Create info to reorient s1 (Scanner1) to s0
    """
    for p0, p1, similarity in similar:
        for rel in similarity:
            try:
                return find_point_reorientation(s0.relmap[p0].rmap[rel], s1.relmap[p1].rmap[rel])
            except Exception as e:
                print(e)
                pass
    raise Exception('No valid similarity found!')


def find_similarity(m0, m1):
    similar = []
    for p0 in m0:
        for p1 in m1:
            similarity = m0[p0].set.intersection(m1[p1].set)
            if len(similarity) > 10:
                similar.append((p0, p1, similarity))
                #print(p0, p1, len(similarity))
    if len(similar) < 12:
        return None
    return similar


def part1(fname):
    data = read_file(fname)
    scanners = [ScannerMap(points) for points in data]
    location = [None] * len(scanners)
    location[0] = Point(0, 0, 0)
    unknown = {i for i in range(len(scanners))}
    # Keying everything of scanner0
    unknown.remove(0)
    to_process = [0]
    while to_process:
        cur = to_process.pop()
        found = []
        for i in unknown:
            similar = find_similarity(scanners[cur].relmap, scanners[i].relmap)
            if not similar:
                continue
            info, offset = find_scanner_reorientation(scanners[cur], scanners[i], similar)
            loc = offset + location[cur]
            print(cur, i, info, offset, loc)
            location[i] = loc
            scanners[i].reorient(info)
            found.append(i)
        to_process.extend(found)
        unknown.difference_update(found)
    beacons = set()
    for scanner, loc in zip(scanners, location):
        for point in scanner.points:
            beacons.add(point + loc)
    print(len(beacons))
    return location


def part2(scanner_locs):
    print(max(p0.dist(p1) for p0, p1 in combinations(scanner_locs, 2)))


def main():
    fname = sys.argv[1]
    scanner_locs = part1(fname)
    part2(scanner_locs)


if __name__ == "__main__":
    main()
