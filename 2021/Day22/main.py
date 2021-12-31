import sys
import re


def read_file(path):
    range_ptn = r'(-?\d+)..(-?\d+)'
    procedure = []

    with open(path, "r") as f:
        for line in f:
            m = re.match(r'(on|off) x={range},y={range},z={range}'.format(range=range_ptn), line)
            state = m.group(1) == 'on'
            ranges = []
            for start, stop in ((m.group(i), m.group(i+1)) for i in range(2, 3*2+1, 2)):
                ranges.append((int(start), int(stop)))
            procedure.append((state, Cuboid(ranges)))
    return procedure


class Cuboid(object):
    def __init__(self, ranges):
        self.ranges = ranges
    
    @property
    def x(self):
        return self.ranges[0]

    @property
    def y(self):
        return self.ranges[1]

    @property
    def z(self):
        return self.ranges[2]

    def __str__(self):
        return str(self.ranges)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.ranges == other.ranges

    def size(self):
        size = 1
        for rg in self.ranges:
            size *= rg[1] - rg[0] + 1
        return size

    def contains_point(self, point):
        for p, self_range in zip(point, self.ranges):
            if not (self_range[0] <= p <= self_range[1]):
                return False
        return True

    def __contains__(self, other):
        if isinstance(other, tuple):
            return self.contains_point(other)
        for other_range, self_range in zip(other.ranges, self.ranges):
            # all ranges must be fully contained
            if other_range[0] < self_range[0] or other_range[1] > self_range[1]:
                return False
        return True
    
    def subtract(self, other):
        overlap = self.overlap(other)
        if not overlap:
            return [self]
        splits = []
        split_from = self
        while (split_from != overlap):
            #find best way to split
            best = (0, None, None)
            for dim in range(3):
                area = split_from.ranges[(dim+1)%3][1] - split_from.ranges[(dim+1)%3][0] + 1
                area *= split_from.ranges[(dim+2)%3][1] - split_from.ranges[(dim+2)%3][0] + 1
                for end in range(2):
                    size = abs(overlap.ranges[dim][end] - split_from.ranges[dim][end]) * area
                    if size > best[0]:
                        best = (size, dim, end)
            #split once, and restart with remainder
            size, dim, end = best
            clean = list(split_from.ranges)
            overlaps = list(split_from.ranges)
            if end == 0:
                clean[dim] = (split_from.ranges[dim][0], overlap.ranges[dim][0] - 1)
                overlaps[dim] = (overlap.ranges[dim][0], split_from.ranges[dim][1])
            else:
                clean[dim] = (overlap.ranges[dim][1] + 1, split_from.ranges[dim][1])
                overlaps[dim] = (split_from.ranges[dim][0], overlap.ranges[dim][1])
            splits.append(Cuboid(clean))
            split_from = Cuboid(overlaps)
        return splits

    def overlap(self, other):
        ranges = []
        for other_range, self_range in zip(other.ranges, self.ranges):
            ranges.append((max(self_range[0], other_range[0]), min(self_range[1], other_range[1])))
            if ranges[-1][0] > ranges[-1][1]:
                return None
        return Cuboid(ranges)

    def overlaps(self, other):
        for other_range, self_range in zip(other.ranges, self.ranges):
            if not (other_range[1] >= self_range[0] and other_range[0] <= self_range[1]):
                return False
        return True


def run_procedure(data):
    lit_cubes = []
    for state, cube in data:
        new_set = []
        for existing in lit_cubes:
            # split any existing cubes so they don't overlap with the new one
            new_set.extend(existing.subtract(cube))
        # add the new cube if it is on, ignore if it is off
        if state:
            new_set.append(cube)
        lit_cubes = new_set
    return lit_cubes


def part1(data):
    init_region = Cuboid([(-50, 50), (-50, 50), (-50, 50)])
    filtered_data = []
    for state, cube in data:
        if cube not in init_region:
            continue
        filtered_data.append((state, cube))
    lit_cubes = run_procedure(filtered_data)
    print(sum(cube.size() for cube in lit_cubes))


def part2(data):
    lit_cubes = run_procedure(data)
    print(sum(cube.size() for cube in lit_cubes))


def quick_test():
    cl = [
        Cuboid([(0,5), (0,2), (0,2)]),
        Cuboid([(1,5), (1,1), (1,1)]),
        #Cuboid([(0,1), (1,2), (2,3)]),
        #Cuboid([(1,2), (2,3), (4,5)]),
    ]
    for i in range(len(cl)):
        for j in range(i+1, len(cl)):
            print(cl[i], cl[j], cl[i].split(cl[j]))
        #for c2 in cl:
        #    print(c1, c2, c1 in c2, c2 in c1)


def main():
    data = read_file(sys.argv[1])
    part1(data)
    part2(data)


if __name__ == "__main__":
    main()
