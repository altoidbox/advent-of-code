

def read_file(path):
    tiles = []
    with open(path, "r") as f:
        g = None
        for line in f:
            line = line.strip()
            if line.startswith('Tile'):
                id_ = int(line[5:9])  # assume "Tile DDDD:"
                g = Grid([], id_)
            elif line:
                g.add_row(line)
            else:
                if g:
                    tiles.append(g)
                g = None
    if g:
        tiles.append(g)
    return tiles


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

    def dist(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3
DIR_NAMES = "TRBL"


class Relationship(object):
    def __init__(self, owner, neighbor, edge, reversed_):
        self.owner = owner
        self.neighbor = neighbor
        self.edge = edge  # 0:TOP, 1:RIGHT, 2:BOTTOM, 3:LEFT
        self.reversed = reversed_

    def flip_v(self):
        if self.edge == TOP or self.edge == BOTTOM:
            self.edge = (self.edge + 2) % 4
        self.reversed = not self.reversed
        n_rel = self.neighbor.rel_tile(self.owner)
        n_rel.reversed = not n_rel.reversed

    def flip_h(self):
        if self.edge == LEFT or self.edge == RIGHT:
            self.edge = (self.edge + 2) % 4
        self.reversed = not self.reversed
        n_rel = self.neighbor.rel_tile(self.owner)
        n_rel.reversed = not n_rel.reversed

    def rotate_r(self):
        self.edge = (self.edge + 1) % 4

    def rotate_l(self):
        self.edge = (self.edge + 3) % 4

    def __str__(self):
        return "{}{}{}".format(DIR_NAMES[self.edge], self.neighbor.id, "R" if self.reversed else "")

    def __repr__(self):
        return str(self)


class Grid(object):
    ADJACENT_DIRS = [p for p in Point.range(Point(-1, -1), Point(1, 1)) if not (p.x == 0 and p.y == 0)]
    PREV_DIRS = ADJACENT_DIRS[:4]
    NEXT_DIRS = ADJACENT_DIRS[4:]

    def __init__(self, values=None, id_=0):
        self.id = id_
        if values is None:
            values = []
        self.values = []
        for row in values:
            self.values.append(list(row))
        self.height = 0
        self.width = 0
        self._init_sizes()
        self._edges = None
        self.neighbors = []

    def add_row(self, row):
        self.values.append(list(row))
        self._init_sizes()

    def append_to_row(self, y, data):
        if self.height == y:
            self.add_row(data)
        else:
            self.values[y].extend(data)
            self._init_sizes()

    def _init_sizes(self):
        self.height = len(self.values)
        self.width = len(self.values[0]) if self.values else 0

    @staticmethod
    def create(width, height, init_val):
        grid = Grid([], 0)
        row = [init_val] * width
        for _ in range(height):
            grid.values.append(list(row))
        grid.height = height
        grid.width = width
        return grid

    def neighbor_at(self, edge):
        rel = self.rel_at(edge)
        if not rel:
            return None
        return rel.neighbor

    def rel_at(self, edge):
        for n in self.neighbors:
            if n.edge == edge:
                return n
        return None

    def rel_tile(self, tile):
        for n in self.neighbors:
            if n.neighbor is tile:
                return n
        return None

    def flip_v(self):
        self.values.reverse()
        for n in self.neighbors:
            n.flip_v()

    def flip_h(self):
        for row in self.values:
            row.reverse()
        for n in self.neighbors:
            n.flip_h()

    def rotate_r(self):
        new_values = []
        for x in range(self.width):
            new_row = []
            for row in reversed(self.values):
                new_row.append(row[x])
            new_values.append(new_row)
        self.values = new_values
        self._init_sizes()
        for n in self.neighbors:
            n.rotate_r()

    def rotate_l(self):
        new_values = []
        for x in reversed(range(self.width)):
            new_row = []
            for row in self.values:
                new_row.append(row[x])
            new_values.append(new_row)
        self.values = new_values
        self._init_sizes()
        for n in self.neighbors:
            n.rotate_l()

    def orient(self, edge, target):
        diff = target - edge
        if diff < 0:
            diff += 4
        # just want to get a particular edge into a particular position
        if diff == 1:
            self.rotate_r()
        elif diff == 2:
            if edge == TOP or edge == BOTTOM:
                self.flip_v()
            else:  # Must be left or right
                self.flip_h()
        elif diff == 3:
            self.rotate_l()
        n = self.rel_at(target)
        # We want the relationship to be reversed
        if n.reversed:
            return
        elif target == LEFT or target == RIGHT:
            # Flip vertical to keep the neighbor in the same spot, but reverse our orientation
            self.flip_v()
        else:
            # Similar to L/R
            self.flip_h()

    def each_point(self):
        for p in Point.range(Point(0, 0), Point(self.width - 1, self.height - 1)):
            yield p

    def items(self):
        for p in Point.range(Point(0, 0), Point(self.width - 1, self.height - 1)):
            yield p, self[p]

    def edges(self):
        if not self._edges:
            self._edges = []
            self._edges.append(self.values[0])
            right_edge = []
            left_edge = []
            for y in range(len(self.values)):
                left_edge.append(self.values[y][0])
                right_edge.append(self.values[y][-1])
            self._edges.append(right_edge)
            self._edges.append(list(reversed(self.values[-1])))
            left_edge.reverse()
            self._edges.append(left_edge)

        return (edge for edge in self._edges)

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


def find_edge_matches(tiles):
    corners = []
    for tile in tiles:
        misses = 0
        for ei, edge in enumerate(tile.edges()):
            edge_reversed = list(reversed(edge))
            matches = []
            for other_tile in tiles:
                if tile == other_tile:
                    continue
                for oei, other_edge in enumerate(other_tile.edges()):
                    if edge == other_edge:
                        tile.neighbors.append(Relationship(tile, other_tile, ei, False))
                        matches.append("F{}:{}".format(other_tile.id, oei))
                    if edge_reversed == other_edge:
                        tile.neighbors.append(Relationship(tile, other_tile, ei, True))
                        matches.append("R{}:{}".format(other_tile.id, oei))
            # print("{}:{} => {}".format(tile.id, ei, matches))
            if len(matches) == 0:
                misses += 1
        if misses > 2:
            raise Exception("found non-matching piece")
        elif misses == 2:
            corners.append(tile)
    return corners


def part1(path):
    tiles = read_file(path)
    corners = find_edge_matches(tiles)
    print("Corners: ", list(g.id for g in corners))
    answer = 1
    for corner in corners:
        answer *= corner.id
    print(answer)
    return tiles, corners


def orient_to(fixed_tile, fixed_tile_side):
    tile_rel = fixed_tile.rel_at(fixed_tile_side)
    if not tile_rel:
        return None
    # to our side, we need to orient that tile to match us, so that we are on its opposite side
    other_rel = tile_rel.neighbor.rel_tile(fixed_tile)
    tile_rel.neighbor.orient(other_rel.edge, (fixed_tile_side + 2) % 4)
    return tile_rel.neighbor


def build_row(left_tile):
    cur_tile = left_tile
    while cur_tile:
        cur_tile = orient_to(cur_tile, RIGHT)


MONSTER = Grid([
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
])


def active_points(g):
    result = []
    for p, v in g.items():
        if v == '#':
            result.append(p)
    return result


def find_monster(m, image):
    m_points = active_points(m)
    count = 0
    for p_image in Point.range(Point(0, 0), Point(image.width - m.width, image.height - m.height)):
        if all(image[p_image + p] == '#' for p in m_points):
            count += 1
    return count


def find_monster_any_rotation(m, image):
    for _ in range(2):
        for _ in range(4):
            num_found = find_monster(m, image)
            if num_found:
                return num_found
            m.rotate_r()
        m.flip_h()
    return 0


def part2(path):
    tiles = read_file(path)
    corners = find_edge_matches(tiles)
    # for tile in tiles:
    #    print("{}: {}".format(tile.id, tile.neighbors))
    print("Stitching image...")
    top_left = corners[0]
    # orient so that there is a blank on the left and top
    if top_left.rel_at(LEFT) is not None:
        top_left.flip_h()
    if top_left.rel_at(TOP) is not None:
        top_left.flip_v()
    # now, build the top row
    row_start = top_left
    while row_start:
        build_row(row_start)
        row_start = orient_to(row_start, BOTTOM)

    full_image = Grid()
    col_start = top_left
    # for each column
    while col_start:
        y = 0
        cur_tile = col_start
        while cur_tile:
            for row in cur_tile.values[1:-1]:
                full_image.append_to_row(y, row[1:-1])
                y += 1
            cur_tile = cur_tile.neighbor_at(BOTTOM)
        col_start = col_start.neighbor_at(RIGHT)
    # print(full_image)
    monster_count = find_monster_any_rotation(MONSTER, full_image)
    print(monster_count, "monsters")
    hash_count = 0
    for p, v in full_image.items():
        if v == '#':
            hash_count += 1
    hash_count -= monster_count * len(active_points(MONSTER))
    print(hash_count, "roughness")


def main():
    part1("example.txt")
    part2("example.txt")
    part1("input.txt")
    part2("input.txt")


if __name__ == "__main__":
    main()
