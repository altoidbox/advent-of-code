import re

FILE = "input.txt"
#FILE = "example.txt"


def read_file(path):
    with open(path, "r") as f:
        data = list(map(lambda s: s.strip(), f))
    return parse(data)


def parse(data):
    answers = []
    cur = []
    for line in data:
        if not line:
            if cur:
                answers.append(cur)
                cur = []
            continue
        cur.append(line)
    if cur:
        answers.append(cur)
    return answers


def add_answers(group, idx, line):
    for c in line:
        group.setdefault(c, set()).add(idx)


def part1():
    data = read_file(FILE)
    groups = []
    for answers in data:
        g = {}
        for i, entry in enumerate(answers):
            add_answers(g, i, entry)
        groups.append(g)

    print("{} groups, {} yeses".format(len(groups), sum(len(g) for g in groups)))


def part2():
    data = read_file(FILE)
    groups = []
    for answers in data:
        g = {}
        for i, entry in enumerate(answers):
            add_answers(g, i, entry)
        groups.append((len(answers), g))
    total = 0
    for count, g in groups:
        for who in g.values():
            if len(who) == count:
                total += 1
    print("{} groups, {} yeses".format(len(groups), total))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
