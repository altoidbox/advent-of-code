import re

FILE = "input.txt"
#FILE = "example.txt"
#FILE = "invalid.txt"
#FILE = "valid.txt"


required = {
    "byr": lambda v: 1920 <= int(v) <= 2002,
    "iyr": lambda v: 2010 <= int(v) <= 2020,
    "eyr": lambda v: 2020 <= int(v) <= 2030,
    "hgt": lambda v:
        150 <= int(v[:-2]) <= 193 if v.endswith("cm") else 59 <= int(v[:-2]) <= 76 if v.endswith("in") else False,
    "hcl": lambda v: re.match(r'^#[0-9a-f]{6}$', v) is not None,
    "ecl": lambda v: v in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    "pid": lambda v: re.match(r'^[0-9]{9}$', v) is not None,
    #"cid",
}


def read_file(path):
    with open(path, "r") as f:
        data = list(map(lambda s: s.strip(), f))
    return parse(data)


def parse(data):
    passports = []
    cur = {}
    for line in data:
        if not line:
            #print(is_valid(cur), cur)
            passports.append(cur)
            cur = {}
            continue
        for item in line.split(" "):
            key, value = item.split(":")
            cur[key] = value
    if cur:
        passports.append(cur)
    return passports


def is_valid(passport):
    rq = list(required)
    for key in passport.keys():
        if key == 'cid':
            continue
        rq.remove(key)
    if len(rq):
        print(passport, "missing: ", rq)
        return False
    return True


def is_valid2(passport):
    invalid = []
    rq = dict(required)
    for key, value in passport.items():
        if key == 'cid':
            continue
        try:
            if not rq[key](value):
                raise Exception()
        except:
            invalid.append((key, value))
        del rq[key]

    if len(rq):
        print(passport, "missing: ", rq.keys())
        return False
    if len(invalid):
        print(passport, "invalid: ", invalid)
        return False
    return True


def part1():
    data = read_file(FILE)
    result = len(list(filter(None, (is_valid(p) for p in data))))
    print("{}/{}".format(result, len(data)))


def part2():
    data = read_file(FILE)
    result = len(list(filter(None, (is_valid2(p) for p in data))))
    print("{}/{}".format(result, len(data)))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
