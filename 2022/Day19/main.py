#!/usr/bin/env python3
import argparse
import re
import math
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class Blueprint(object):
    def __init__(self, num):
        self.num = num
        self.robots = {}
    
    def cost(self, type_):
        return self.robots[type_]

    def __repr__(self):
        return '{}: {}'.format(self.num, self.robots)


def load(path):
    blueprints = []
    with open(args.input, "r") as f:
        for line in f:
            match = re.search(r'Blueprint (\d+)', line)
            if match:
                blueprints.append(Blueprint(int(match.group(1))))
            match = re.search(r'Each (ore) robot costs (\d+) (\w+).', line)
            if match:
                blueprints[-1].robots[match.group(1)] = { match.group(3): int(match.group(2)) }
            match = re.search(r'Each (clay) robot costs (\d+) (\w+).', line)
            if match:
                blueprints[-1].robots[match.group(1)] = { match.group(3): int(match.group(2)) }
            match = re.search(r'Each (obsidian) robot costs (\d+) (\w+) and (\d+) (\w+).', line)
            if match:
                blueprints[-1].robots[match.group(1)] = { 
                    match.group(3): int(match.group(2)),
                    match.group(5): int(match.group(4))
                }
            match = re.search(r'Each (geode) robot costs (\d+) (\w+) and (\d+) (\w+).', line)
            if match:
                blueprints[-1].robots[match.group(1)] = { 
                    match.group(3): int(match.group(2)),
                    match.group(5): int(match.group(4))
                }
            
    return blueprints


def print_cost(cost):
    msg = ''
    for i, (t, q) in enumerate(cost.items()):
        if i == 0:
            prefix = ''
        elif len(cost) - 1 != i:
            prefix = ', '
        else:
            prefix = ' and '
        msg += f'{prefix}{q} {t}'
    return msg


def time_until(bp, type_, resources, production):
    minutes = 0
    for t, q in bp.robots[type_].items():
        need = q - resources[t]
        if need > 0:
            if production[t] == 0:
                return float('inf')
            minutes = max(minutes, need / production[t])
    return math.ceil(minutes)


def sim_build(bp, want, type_, resources, production):
    dont = time_until(bp, want, resources, production)
    for t, q in bp.robots[type_].items():
        resources[t] -= q
    production[type_] += 1
    do = time_until(bp, want, resources, production)
    for t, q in bp.robots[type_].items():
        resources[t] += q
    production[type_] -= 1
    return do <= dont


def build(bp, type_, resources, production):
    cost = bp.robots[type_]
    deficit = Counter()
    for t, q in cost.items():
        need = q - resources[t]
        if need > 0:
            deficit[t] = need
    if not deficit:
        print(f'Spend {print_cost(cost)} to start building a {type_}-collecting robot.')
        for t, q in cost.items():
            resources[t] -= q
        
        return Counter({type_ : 1})
    else:
        to_build = deficit.most_common(1)[0][0]
        if to_build == type_ or not sim_build(bp, type_, to_build, resources, production):
            return Counter()
        return build(bp, to_build, resources, production)


def collect(production, resources):
    for mat, qty in production.items():
        if qty == 0:
            continue
        resources[mat] += qty
        if qty > 1:
            s0 = 's'
            s1 = ''
        else:
            s0 = ''
            s1 = 's'
        print(f'{qty} {mat}-collecting robot{s0} collect{s1} {qty} {mat}; you now have {resources[mat]} {mat}.')


def simulate(bp, minutes=24):
    resources = Counter()
    production = Counter(ore=1)
    goal = 'geode'
    for m in range(minutes):
        print(f'== Minute {m+1} ==')
        building = build(bp, goal, resources, production)
        collect(resources, production)
        for t, q in building.items():
            production[t] += q
            print(f'The new {t}-collecting robot is ready; you now have {production[t]} of them.')
        print()
    return resources[goal]


def start_build(bp, type_, resources, refund=False):
    cost = bp.robots[type_]
    if not refund:
        for mat, amt in cost.items():
            if amt > resources[mat]:
                return False
    sign = 1 if refund else -1
    for mat, amt in cost.items():
        resources[mat] += sign * amt
    return True


def produce(resources, production, sign):
    for mat, amt in production.items():
        resources[mat] += sign * amt


def sim_all(bp, minutes, resources, production, goal):
    if minutes == 0:
        return resources[goal]
        
    produce(resources, production, 1)
    best = sim_all(bp, minutes - 1, resources, production, goal)
    produce(resources, production, -1)

    for type_ in bp.robots.keys():
        if start_build(bp, type_, resources):
            produce(resources, production, 1)
            production[type_] += 1
            #print(f'{minutes}: {type_}')
            cur = sim_all(bp, minutes - 1, resources, production, goal)
            production[type_] -= 1
            produce(resources, production, -1)
            start_build(bp, type_, resources, refund=True)
            if cur > best:
                best = cur
    return best


def part1(data):
    print(data)
    for bp in data:
        best = simulate(bp)
        # best = sim_all(bp, 24, Counter(), Counter(ore=1), 'geode')
        print(bp.num, best)


def part2(data):
    pass

data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

