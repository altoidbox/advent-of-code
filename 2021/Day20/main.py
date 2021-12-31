import sys
import heapq


def read_file(path):
    with open(path, "r") as f:
        algo = f.readline().strip()
        f.readline()
        return algo, Image([s.strip() for s in f])


class Image(object):
    def __init__(self, rows, default='.'):
        self.default = default
        self.rows = []
        for row in rows:
            self.rows.append(list(row))

    @property
    def width(self):
        return len(self.rows[0])

    @property
    def height(self):
        return len(self.rows)

    def valueof(self, px, py):
        v = 0
        #print(px, py, end=' ')
        for y in range(py-1, py+2):
            for x in range(px-1, px+2):
                c = self.getxy(x, y, self.default)
                #print(c, end='')
                v <<= 1
                if c == '#':
                    v += 1
        #print('\n', v)
        return v

    def getxy(self, x, y, default):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return default
        return self.rows[y][x]

    def __str__(self):
        return '\n'.join(''.join(str(v) for v in row) for row in self.rows)

    def values(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield self.rows[y][x]


def enhance(image, algo):
    rows = []
    for y in range(-1, image.height + 1):
        row = []
        for x in range(-1, image.width + 1):
            row.append(algo[image.valueof(x, y)])
        rows.append(row)
    default = algo[image.valueof(-3, -3)]
    return Image(rows, default)


def part1(fname):
    algo, image = read_file(fname)
    for _ in range(2):
        #print(image)
        image = enhance(image, algo)
    print(sum(1 if v == '#' else 0 for v in image.values()))


def part2(fname):
    algo, image = read_file(fname)
    for _ in range(50):
        image = enhance(image, algo)
    print(sum(1 if v == '#' else 0 for v in image.values()))


if __name__ == "__main__":
    part1(sys.argv[1])
    part2(sys.argv[1])
