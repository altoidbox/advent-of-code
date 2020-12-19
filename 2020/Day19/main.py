

def read_file(path):
    rules = {}
    comms = []
    with open(path, "r") as f:
        reading_rules = True
        for line in f:
            line = line.strip()
            if reading_rules:
                if not line:
                    reading_rules = False
                    continue
                rule_num, rule = line.split(": ")
                rule_num = int(rule_num)
                if rule[0] == '"':
                    rules[rule_num] = rule[1]
                else:
                    subrules = rule.split(' | ')
                    parts = []
                    for subrule in subrules:
                        parts.append(list(map(int, subrule.split(" "))))
                    rules[rule_num] = parts
            else:
                comms.append(line)
    return rules, comms


def flatten(rules, rid, flattened):
    if rid in flattened:
        return flattened[rid]
    cur_rule = rules[rid]
    if not isinstance(cur_rule, list):
        flattened[rid] = {cur_rule}
        return flattened[rid]
    all_possible = set()
    for rule_set in cur_rule:
        prefixes = {''}
        for subrule in rule_set:
            children = flatten(rules, subrule, flattened)
            new_prefixes = set()
            for prefix in prefixes:
                for child in children:
                    new_prefixes.add(prefix + child)
            prefixes = new_prefixes
        all_possible.update(prefixes)
    flattened[rid] = all_possible
    return all_possible


def check(rules, rid, val, idx, path):
    if idx >= len(val):
        return 0
    cur_rule = rules[rid]
    if not isinstance(cur_rule, list):
        return 1 if val[idx] == cur_rule else 0
    for i, rule_set in enumerate(cur_rule):
        match_len = 0
        path_len = len(path)
        path.append((rid, i, idx))
        for subrule in rule_set:
            subrule_match_len = check(rules, subrule, val, idx + match_len, path)
            if not subrule_match_len:
                match_len = 0
                break
            match_len += subrule_match_len
        if match_len:
            return match_len
        # remove that path
        while len(path) > path_len:
            path.pop()
    return 0


def part1(path):
    rules, comms = read_file(path)
    # print(rules)
    valid = []
    for value in comms:
        if check(rules, 0, value, 0, []) == len(value):
            valid.append(value)
    print(len(valid))


def part2(path):
    rules, comms = read_file(path)
    # rule[0] = [8, 11]
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    flattened = {}
    set42 = flatten(rules, 42, flattened)
    set31 = flatten(rules, 31, flattened)
    len42 = set(map(len, set42)).pop()
    len31 = set(map(len, set31)).pop()
    # and now we're going to apply the rules manually instead of generically
    valid = []
    for value in comms:
        orig_value = value
        count31 = 0
        count42 = 0
        while value[-len31:] in set31:
            count31 += 1
            value = value[:-len31]
        while value[-len42:] in set42:
            count42 += 1
            value = value[:-len42]
        if not value and count42 > count31 > 0:
            valid.append(orig_value)
    # for v in valid:
    #     print(v)
    print(len(valid))


def main():
    # part1("example2.txt")
    part1("input.txt")
    # part2("example2.txt")
    part2("input.txt")


if __name__ == "__main__":
    main()
