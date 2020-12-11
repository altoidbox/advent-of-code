FILE = "input.txt"
#FILE = "example1.txt"
#FILE = "example2.txt"


def read_file(path):
    with open(path, "r") as f:
        data = list(f)
    return list(line.strip().split(")") for line in data)


def dfs(tree, cur, depth):
    total = 0
    for child in tree.get(cur, []):
        total += dfs(tree, child, depth + 1)
    # number of orbits is 1 for parent + (depth - 1) for all of its parents
    return total + depth


def part1():
    data = read_file(FILE)
    orbits = {}
    for parent, child in data:
        orbits.setdefault(parent, set()).add(child)

    print("{}".format(dfs(orbits, 'COM', 0)))


def path_to_root(parents, start):
    path_to_root = []
    cur = start
    while cur != 'COM':
        cur = parents[cur]
        path_to_root.append(cur)
    return list(reversed(path_to_root))


def part2():
    data = read_file(FILE)
    orbits = {}
    parents = {}
    for parent, child in data:
        parents[child] = parent
        orbits.setdefault(parent, set()).add(child)

    my_path_to_root = path_to_root(parents, 'YOU')
    santa_path_to_root = path_to_root(parents, 'SAN')
    for i, (my, santa) in enumerate(zip(my_path_to_root, santa_path_to_root)):
        if my != santa:
            break
    print("My path", my_path_to_root)
    print("Santa path", santa_path_to_root)
    print("{}".format(len(my_path_to_root[i:] + santa_path_to_root[i:])))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
