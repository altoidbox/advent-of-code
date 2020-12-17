import re

FILE = "input.txt"
# FILE = "example1.txt"
# FILE = "example2.txt"


class MultiRange(object):
    def __init__(self, *ranges):
        self.ranges = ranges

    def __contains__(self, item):
        for rg in self.ranges:
            if item in rg:
                return True
        return False


def read_file(path):
    with open(path, "r") as f:
        rules = {}
        my_ticket = None
        tickets = []
        state = 0
        for line in f:
            line = line.strip()
            if not line:
                state += 1
                continue
            if state == 0:
                vals = re.match(r'^([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)$', line).groups()
                name = vals[0]
                s1, e1, s2, e2 = map(int, vals[1:])
                rules[name] = MultiRange(range(s1, e1+1), range(s2, e2+1))
            elif state == 1:
                if "ticket" in line:
                    state += 1
            elif state == 2:
                my_ticket = list(map(int, line.split(',')))
            elif state == 3:
                if "ticket" in line:
                    state += 1
            else:
                tickets.append(list(map(int, line.split(','))))

        return rules, my_ticket, tickets


def part1():
    rules, my_ticket, tickets = read_file(FILE)
    error_rate = 0
    for ticket in tickets:
        for val in ticket:
            inrange = False
            for rule in rules.values():
                if val in rule:
                    inrange = True
                    break
            if not inrange:
                error_rate += val
    print("part1:", error_rate)


def part2():
    rules, my_ticket, tickets = read_file(FILE)
    valid_tickets = []
    for ticket in tickets:
        for val in ticket:
            inrange = False
            for rule in rules.values():
                if val in rule:
                    inrange = True
                    break
            if not inrange:
                break
        if inrange:
            valid_tickets.append(ticket)
    valid_rules = {}
    for i, _ in enumerate(my_ticket):
        for name, rule in rules.items():
            valid = True
            for ticket in valid_tickets:
                if ticket[i] not in rule:
                    valid = False
                    break
            if valid:
                valid_rules.setdefault(i, set()).add(name)
        if i not in valid_rules:
            print("Found no valid rules for", i)
            return
    # print(len(valid_tickets), "valid out of", len(tickets))
    # for i in range(len(my_ticket)):
    #     print(i, valid_rules[i])
    correct_rules = {}
    while len(correct_rules) < len(rules):
        # First, choose a rule that has only 1 possibility
        chosen = None
        for i, names in valid_rules.items():
            if len(names) == 1:
                chosen = names.pop()
                correct_rules[i] = chosen
                valid_rules.pop(i)
                break
        if not chosen:
            print("!! No valid choice!", valid_rules)
        # Then, remove that value from validity for the remaining rules
        for names in valid_rules.values():
            names.remove(chosen)
        # Then, cycle back
    answer = 1
    for i in range(len(my_ticket)):
        # print(i, correct_rules[i])
        if correct_rules[i].startswith("departure"):
            answer *= my_ticket[i]
    print("part2:", answer)



def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
