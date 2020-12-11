import re


class Entry(object):
    def __init__(self, min, max, c, pw):
        self.min = min
        self.max = max
        self.c = c
        self.pw = pw

    @property
    def valid(self):
        return self.pw.count(self.c) in range(self.min, self.max + 1)

    @property
    def valid2(self):
        if self.max > len(self.pw):
            return False
        return (self.pw[self.min-1] + self.pw[self.max-1]).count(self.c) == 1

    @staticmethod
    def from_str(str_):
        m = re.match(r'(\d+)-(\d+) (\w): (\w+)', str_)
        return Entry(int(m[1]), int(m[2]), m[3], m[4])


def read_file(path):
    with open(path, "r") as f:
        return list(map(Entry.from_str, f))


def part1():
    data = read_file("input.txt")
    print("{} valid / {}".format(len(list(filter(None, (e.valid for e in data)))), len(data)))


def part2():
    data = read_file("input.txt")
    print("{} valid / {}".format(len(list(filter(None, (e.valid2 for e in data)))), len(data)))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()