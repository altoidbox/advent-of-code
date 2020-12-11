import re


FILE = "input.txt"
#FILE = "example2.txt"


def read_file(path):
    with open(path, "r") as f:
        data = list(map(lambda s: s.strip(), f))
    return data


def parse_rule(line):
    container, rules = re.match(r'^(.*) bags contain (.*)\.$', line).groups()
    parsed = {}
    for rule in rules.split(","):
        try:
            count, color = re.match(r'^(\d+) (.*) bags?$', rule.strip()).groups()
        except AttributeError:
            if rule == "no other bags":
                break
            raise
        if color in parsed:
            print("extra rule for {} ({})".format(container, color))
        parsed[color] = int(count)
    return container, parsed


def parse_rules(data):
    all_rules = {}
    for line in data:
        container, bag_rules = parse_rule(line)
        if container in all_rules:
            print("extra rule for {}".format(container))
        all_rules[container] = bag_rules
    return all_rules


def part1():
    all_rules = parse_rules(read_file(FILE))
    parent_bags = {}
    for bag, child_bags in all_rules.items():
        for child_bag in child_bags.keys():
            parent_bags.setdefault(child_bag, set()).add(bag)
    # print(parent_bags)
    holding_bags = set()
    stack = {'shiny gold'}
    while len(stack) > 0:
        cur = stack.pop()
        holding_bags.add(cur)
        for parent in parent_bags.get(cur, []):
            if parent not in holding_bags:
                stack.add(parent)
    # print(holding_bags)
    print(len(holding_bags) - 1)


def count_bags(pre_calc, rules, bag):
    if bag in pre_calc:
        return pre_calc[bag]
    total = 0
    for child, count in rules[bag].items():
        total += (1 + count_bags(pre_calc, rules, child)) * count
    pre_calc[bag] = total
    print("{} = {} inside".format(bag, total))
    return total


def part2():
    all_rules = parse_rules(read_file(FILE))
    print(count_bags({}, all_rules, 'shiny gold'))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
