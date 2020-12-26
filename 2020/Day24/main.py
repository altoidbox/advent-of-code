from collections import defaultdict


def read_file(path):
    paths = []
    with open(path, "r") as f:
        specifier = ''
        for line in f:
            path = []
            for c in line:
                if c in 'ns':
                    specifier = c
                elif c in 'ew':
                    path.append(specifier + c)
                    specifier = ''
            paths.append(path)
    return paths


DIR_MAP = {
    'ne': lambda p: p.north_east(),
    'e': lambda p: p.east(),
    'se': lambda p: p.south_east(),
    'nw': lambda p: p.north_west(),
    'w': lambda p: p.west(),
    'sw': lambda p: p.south_west()
}


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(self.tuple)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)

    def east(self):
        return Point(self.x + 1, self.y)

    def north_east(self):
        mod = self.y % 2
        return Point(self.x + mod, self.y - 1)

    def south_east(self):
        mod = self.y % 2
        return Point(self.x + mod, self.y + 1)

    def west(self):
        return Point(self.x - 1, self.y)

    def north_west(self):
        nmod = not(self.y % 2)
        return Point(self.x - nmod, self.y - 1)

    def south_west(self):
        nmod = not(self.y % 2)
        return Point(self.x - nmod, self.y + 1)

    def adjacent(self):
        for f in DIR_MAP.values():
            yield f(self)

    @property
    def tuple(self):
        return self.x, self.y


def part1(path):
    paths = read_file(path)
    points = {}
    for path in paths:
        cur = Point(0, 0)
        for dir_ in path:
            cur = DIR_MAP[dir_](cur)
        if points.setdefault(cur, False):
            del points[cur]
        else:
            points[cur] = True
    print(len(points))
    return points


def count_adjacent(points):
    adjacency = defaultdict(lambda: 0)
    for p in points:
        adjacency[p] += 0  # make sure every black tile is in the adjacency map, even if it has 0 adjacent black tiles
        for adj in p.adjacent():
            adjacency[adj] += 1
    return adjacency


def part2(points):
    for day in range(100):
        new_points = {}
        adjacency = count_adjacent(points)
        for tile, count in adjacency.items():
            # any tile with 2 adjacent black becomes (or stays) black
            # a black tile with 1 adjacent black also stays black
            # don't track white tiles
            if count == 2 or (count == 1 and tile in points):
                new_points[tile] = True
        points = new_points
    print(len(points))


def main():
    part2(part1("example.txt"))
    part2(part1("input.txt"))


if __name__ == "__main__":
    main()
