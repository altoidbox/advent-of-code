import math

FILE = "input.txt"
# FILE = "example1.txt"
# FILE = "example2.txt"


def read_file(path):
    data = [0, 0]
    with open(path, "r") as f:
        data[0] = int(f.readline())
        data[1] = f.readline().split(',')
    return data


def part1():
    data = read_file(FILE)
    arrival = data[0]
    busses = list(map(int, filter(lambda x: x != 'x', data[1])))
    waits = list(map(lambda bus: bus - (arrival % bus), busses))
    min_wait = min(waits)
    min_bus = busses[waits.index(min_wait)]
    print(min_bus, min_wait, min_wait * min_bus)


# x * b[0] = y == answer
# x = 11 (mod 13)
# x = 11 + 13r
# x = 50 (mod 59)
# 11 + 13r = 50 (mod 59)
# 13r = 39 (mod 59)

# x %  41 =   25
# x %  37 =    8
# x % 419 =  418
# x %  19 =   18
# x %  23 =   22
# x %  29 =   28
# x % 421 =   29
# x %  17 =   11


def solve_mod(a1, n1, a2, n2):
    x = a1
    while x % n2 != a2:
        x += n1
    return x, n1 * n2


def part2():
    data = read_file(FILE)
    busses = list(map(lambda x: 0 if x == 'x' else int(x), data[1]))
    print(busses)
    base = busses[0]
    congruences = []
    for i, b in enumerate(busses):
        if i == 0 or b == 0:
            continue
        # x * base == y * b - i
        # x = (y * b - i) / base
        x = y = 1
        xv = base
        yv = b - i
        while xv != yv:
            if xv < yv:
                x += 1
                xv += base
            else:
                y += 1
                yv += b
        congruences.append((b, x))
    # Use Chinese Remainder Theorem to solve system of modular congruences
    congruences = list(sorted(congruences))
    for mod, rem in congruences:
        print("x ~= {:3} (mod {:3})".format(rem, mod))
    mod, rem = congruences.pop()
    while congruences:
        mod1, rem1 = congruences.pop()
        rem, mod = solve_mod(rem, mod, rem1, mod1)
    print(rem, rem * base)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
