import argparse
from datetime import datetime
import re
from collections import deque


class Point(object):
    def __init__(self, y, x):
        self.x = x
        self.y = y

    @property
    def tuple(self):
        return self.y, self.x

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.y + other.y, self.x + other.x)
        elif isinstance(other, (list, tuple)) and len(other) == 2:
            return Point(self.y + other[0], self.x + other[1])
        raise ValueError()

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, (list, tuple)) and len(other) == 2:
            return self.y == other[0] and self.x == other[1]
        return False


def y(point):
    return point[0]


def x(point):
    return point[1]


def add_points(left, right):
    return left[0] + right[0], left[1] + right[1]


ADJACENTS = ((-1, 0), (0, -1), (0, 1), (1, 0))


def get_adjacents(grid, point, type_):
    values = []
    for offs in ADJACENTS:
        p = add_points(point, offs)
        if y(p) in range(len(grid)) and y(p) in range(len(grid[y(p)])):
            if grid[y(p)][x(p)] == type_:
                values.append(p)
    return values


def find_first_move(moves, end_point):
    move = end_point
    depth, edge = moves[move]
    while depth > 1:
        # print("{}: {}".format(depth, move))
        move = edge
        depth, edge = moves[move]
    # print("{}: {}*".format(depth, move))
    return move


def resolve_move_tie(moves, opt1, opt2):
    opt1_start = find_first_move(moves, opt1)
    opt2_start = find_first_move(moves, opt2)
    if opt1_start <= opt2_start:
        return opt1
    print("Opt2 wins tie!")
    return opt2


class Army(object):
    def __init__(self, name):
        self.name = name
        self.groups = set()

    def __str__(self):
        out = self.name + ':\n'
        for group in self.groups:
            out += str(group) + '\n'
        return out


class Group(object):
    def __init__(self, army, num_units, hp, ap, attack_type, initiative, weaknesses, immunities, id_):
        self.army = army
        self.num_units = num_units
        self.hp = hp
        self.ap = ap
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.id = id_

    def __str__(self):
        #337 units each with 6482 hit points (weak to radiation, fire; immune to cold, bludgeoning) with an attack that does 189 slashing damage at initiative 15
        return "{} units each with {} hit points (weak to {}; immune to {}) with an attack that does {} {} damage at initiative {}".format(
            self.num_units, self.hp, ', '.join(self.weaknesses), ', '.join(self.immunities), self.ap, self.attack_type, self.initiative
        )

    @property
    def effective_power(self):
        return self.num_units * self.ap

    def damage_against(self, other):
        if self.attack_type in other.weaknesses:
            power = self.ap * 2
        elif self.attack_type in other.immunities:
            power = 0
        else:
            power = self.ap
        return power * self.num_units

    def attack(self, other):
        damage = self.damage_against(other)
        killed = damage / other.hp
        killed = min(killed, other.num_units)
        #print("{} group {} attacks defending group {} killing {} units".format(
        #    self.army, self.id, other.id, killed))
        other.num_units -= killed
        return killed

    def choose_target(self):
        pass


class StaleMate(Exception):
    pass


class Game:
    def __init__(self, part2=False):
        self.armies = {}
        self.opponents = {}
        self.groups = set()
        self.army_names = []

    def __str__(self):
        out = ''
        for army in self.armies.values():
            out += str(army) + '\n'
        return out

    def summary(self):
        out = ''
        for army in self.armies.values():
            out += army.name + ':\n'
            for group in sorted(army.groups, key=lambda g: g.id):
                out += "Group {} contains {} units\n".format(group.id, group.num_units)
        return out

    def setup(self):
        self.army_names = list(self.armies.keys())
        self.opponents[self.army_names[0]] = self.armies[self.army_names[1]]
        self.opponents[self.army_names[1]] = self.armies[self.army_names[0]]

    def targeting_phase(self):
        opponent_groups = {
            self.army_names[0]: self.opponents[self.army_names[0]].groups.copy(),
            self.army_names[1]: self.opponents[self.army_names[1]].groups.copy()
        }
        matchups = {}
        for group in sorted(self.groups, key=lambda g: (g.effective_power, g.initiative), reverse=True):
            if len(opponent_groups[group.army]) == 0:
                continue
            target = max(opponent_groups[group.army], key=lambda other: (group.damage_against(other), other.effective_power, other.initiative))
            if group.damage_against(target) == 0:
                continue
            #print("{} group {} would deal deal defending {} group {} {} damage".format(
            #    group.army, group.id, target.army, target.id, group.damage_against(target)))
            opponent_groups[group.army].remove(target)
            matchups[group] = target
        return matchups

    def remove_player(self, group):
        self.groups.remove(group)
        self.armies[self.army_names[0]].groups.discard(group)
        self.armies[self.army_names[1]].groups.discard(group)

    def round(self, quiet=False):
        matchups = self.targeting_phase()
        killed = 0
        for attacker in sorted(matchups.keys(), key=lambda a: a.initiative, reverse=True):
            target = matchups.pop(attacker, None)
            if target is None:
                continue
            killed += attacker.attack(target)
            if target.num_units == 0:
                self.remove_player(target)
                matchups.pop(target, None)
        if killed == 0:
            raise StaleMate()

    def calc(self):
        return sum(group.num_units for group in self.groups)

    def play(self, quiet=False):
        self.setup()
        if not quiet:
            print(self)
        while True:
            # print("Round {} Begin: ".format(rounds_completed + 1))
            self.round()
            if any(len(army.groups) == 0 for army in self.armies.values()):
                break
            if not quiet:
                print(self.summary())
        if not quiet:
            print(self.summary())
        # print(self.calc())


def load(input):
    # 337 units each with 6482 hit points (weak to radiation, fire; immune to cold, bludgeoning) with an attack that does 189 slashing damage at initiative 15
    group_re = r'(\d+) units? each with (\d+) hit points? (\(.*\))? ?with an attack that does (\d+) (.*) damage at initiative (\d+)'
    sp_re = r'(.*) to (.*)'
    game = Game()
    cur_army = None
    with open(input, 'r') as f:
        for line in f:
            line = line.strip()
            if line.endswith(':'):
                cur_army = Army(line.strip(':'))
                game.armies[cur_army.name] = cur_army
            elif line:
                units, hp, all_sp, ap, attack_type, initiative = re.match(group_re, line).groups()
                sp_dict = {}
                if all_sp:
                    for sp in all_sp.strip('()').split('; '):
                        sp_class, sp_types = re.match(sp_re, sp).groups()
                        sp_dict[sp_class] = sp_types.split(', ')
                cur_army.groups.add(
                    Group(cur_army.name, int(units), int(hp), int(ap), attack_type, int(initiative),
                          sp_dict.get('weak', []), sp_dict.get('immune', []), len(cur_army.groups) + 1))
    for army in game.armies.values():
        game.groups.update(army.groups)
    return game


def part1(args):
    game = load(args.input)
    print(game)
    game.play(quiet=True)


def part2(args):
    min_boost = 4
    max_boost = 10000
    solutions = {}
    while True:
        game = load(args.input)
        chosen_boost = (max_boost + min_boost) / 2
        for group in game.armies['Immune System'].groups:
            group.ap += chosen_boost
        try:
            game.play(True)
            print("Immune system {} with {} boost".format(
                'wins' if len(game.armies['Immune System'].groups) else 'loses', chosen_boost))
            if len(game.armies['Immune System'].groups):
                max_boost = chosen_boost
                solutions[chosen_boost] = game.calc()
            else:
                min_boost = chosen_boost + 1
        except StaleMate:
            print("Immune system {} with {} boost".format('ties', chosen_boost))
            min_boost = chosen_boost + 1
        if min_boost == max_boost:
            print("Found optimum power {}".format(min_boost))
            print("solution: {}".format(solutions[min_boost]))
            break
        elif min_boost > max_boost:
            print("No solution in range")
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--part2", action="store_true")

    args = parser.parse_args()

    if args.part2:
        part2(args)
    else:
        part1(args)
