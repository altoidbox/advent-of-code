

def test(x):
    has_dup = False
    l = 0
    for c in str(x):
        i = int(c)
        if i == l:
            has_dup = True
        if i < l:
            return False
        l = i
    return has_dup


def test2(x):
    dup_len = 1
    has_dup = False
    l = 0
    strval = str(x)
    for idx, c in enumerate(strval):
        i = int(c)
        if i == l:
            dup_len += 1
            if dup_len == 2 and c != strval[idx+1:idx+2]:
                has_dup = True
        else:
            dup_len = 1
        if i < l:
            return False
        l = i
    return has_dup


def part1():
    print(test(111111))
    print(test(223450))
    print(test(123789))
    count = 0
    for x in range(264360, 746325+1):
        if test(x):
            count += 1
    print("{}".format(count))


def part2():
    print(test2(112233))
    print(test2(123444))
    print(test2(111122))
    count = 0
    for x in range(264360, 746325+1):
        if test2(x):
            count += 1
    print("{}".format(count))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
