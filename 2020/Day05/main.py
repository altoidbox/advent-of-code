FILE = "input.txt"
#FILE = "example3.txt"
#FILE = "invalid.txt"
#FILE = "valid.txt"


def read_file(path):
    with open(path, "r") as f:
        data = list(map(lambda s: s.strip(), f))
    return parse(data)


def find(chrs, botc):
    bot = 0
    top = 2 ** len(chrs) - 1
    for c in chrs:
        if c == botc:
            top = bot + (top - bot) // 2
        else:
            bot = bot + (top - bot) // 2 + 1
        #print(bot, top)
    return bot


def seat_id(r, c):
    return r * 8 + c


def parse(data):
    items = []
    for line in data:
        items.append((find(line[:7], 'F'), find(line[7:], 'L')))
    return items


def part1():
    data = read_file(FILE)
    print(max(seat_id(*p) for p in data))


def next_seat(r, c):
    if c == 7:
        return r + 1, 0
    return r, c + 1


def part2():
    data = sorted(read_file(FILE))
    cur = data[0]
    for seat in data[1:]:
        #print(cur, next_seat(*cur), seat)
        cur = next_seat(*cur)
        if cur != seat:
            print(cur)
            print(seat_id(*cur))
            break


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
