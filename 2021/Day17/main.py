

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

    def __lt__(self, other):
        return self.y < other.y or self.y == other.y and self.x < other.x

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)


def simulate1(start, v):
    end = start + v
    if v.x > 0:
        v.x -= 1
    if v.x < 0:
        v.x += 1
    v.y -= 1
    return end, v


def find_vx(tmin, tmax):
    for x in range(tmax.x + 1):
        v = Point(x, 0)
        p = Point(0, 0)
        while v.x > 0:
            p, v = simulate1(p, v)
            if p.x > tmax.x:
                break
            if p.x >= tmin.x and v.x == 0:
                #print('vx={}'.format(x))
                return x


def find_all_vx(tmin, tmax):
    options = []
    for x in range(tmax.x + 1):
        v = Point(x, 0)
        p = Point(0, 0)
        n = 0
        while v.x > 0:
            p, v = simulate1(p, v)
            n += 1
            if p.x > tmax.x:
                break
            if p.x >= tmin.x:
                options.append(x)
                break
    return options


def find_vy(x, tmin, tmax):
    answer = 0
    for y in range(171):
        maxy = 0
        v = Point(x, y)
        p = Point(0, 0)
        while p.y > tmax.y:
            if p.y > maxy:
                maxy = p.y
            p, v = simulate1(p, v)
            if tmin.y <= p.y <= tmax.y:
                #print(maxy, y, p)
                answer = maxy
    return answer


def find_solutions(x, tmin, tmax):
    solns = []
    for y in range(tmin.y, 0-tmin.y):
        v = Point(x, y)
        p = Point(0, 0)
        while p.y > tmin.y and p.x < tmax.x:
            p, v = simulate1(p, v)
            if tmin.y <= p.y <= tmax.y and tmin.x <= p.x <= tmax.x:
                solns.append(Point(x, y))
                break
    return solns


def part1(tmin, tmax):
    x = find_vx(tmin, tmax)
    y = find_vy(x, tmin, tmax)
    print(y)


def part2(tmin, tmax):
    xopts = find_all_vx(tmin, tmax)
    solns = []
    #print(xopts)
    for x in xopts:
        solns.extend(find_solutions(x, tmin, tmax))
    print(len(solns))


if __name__ == '__main__':
    part1(Point(20, -10), Point(30, -5))
    part1(Point(60, -171), Point(94, -136))
    part2(Point(20, -10), Point(30, -5))
    part2(Point(60, -171), Point(94, -136))
