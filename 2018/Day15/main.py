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


class Player(object):
    def __init__(self, y, x, team, hp, ap):
        self.point = (y, x)
        self.team = team
        self.hp = hp
        self.ap = ap

    def __str__(self):
        return "<{} {}:{}>".format(self.point, self.team, self.hp)

    def generate_targets(self, game):
        targets = set()
        for opponent in game.opponents(self.team):
            for point in get_adjacents(game.grid, opponent.point, '.'):
                targets.add(point)
        return targets

    def try_attack(self, game):
        targets = sorted((game.players[p] for p in get_adjacents(game.grid, self.point, OPPONENTS[self.team])),
                         key=lambda t: t.hp)
        if not targets:
            return False
        else:
            target = targets[0]
            # print("{} attacks {}".format(self, target))
            target.hp -= self.ap
            if target.hp <= 0:
                # print("{} dies".format(target))
                game.remove_player(target)
            return True

    def play(self, game):
        if self.try_attack(game):
            return
        edges = deque()
        edges.append((0, self.point))
        targets = self.generate_targets(game)
        moves = {self.point: (0, self.point)}
        candidates = []
        max_edge_depth = None
        while len(edges):
            depth, edge = edges.popleft()
            if max_edge_depth is not None and depth > max_edge_depth:
                break
            next_moves = get_adjacents(game.grid, edge, '.')
            for move in next_moves:
                if move in moves:
                    continue
                    if moves[move][0] <= depth:
                        continue  # other move is better
                    # for moves in the move list, it should never be possible to find a better move, but we can find ties
                    # I'm not even sure that ties will be found that change hands
                    moves[move] = depth + 1, resolve_move_tie(moves, moves[move], edge)
                else:
                    # print("add {} {} -> {}".format(depth+1, edge, move))
                    moves[move] = depth + 1, edge
                    edges.append((depth + 1, move))
                    if move in targets:
                        candidates.append(move)
                        max_edge_depth = depth
        # Found all shortest paths... Now figure out which one to pursue
        if len(candidates) == 0:
            # No candidates. We obviously didn't attack already. Nothing to do?
            return
        target = min(candidates)
        # print("{} moving toward {}".format(self, target))
        game.move_player(self, find_first_move(moves, target))
        self.try_attack(game)


OPPONENTS = {'G': 'E', 'E': 'G'}


class NoOpponents(Exception):
    pass


class ElfDeath(Exception):
    pass


class Game:
    def __init__(self, part2=False):
        self.teams = {'G': [], 'E': []}
        self.players = {}
        self.grid = []
        self.part2 = part2
        self.rounds_completed = 0

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def opponents(self, team):
        opponents = self.teams[OPPONENTS[team]]
        if len(opponents) == 0:
            raise NoOpponents()
        return opponents

    def add_player(self, player):
        self.players[player.point] = player
        self.teams[player.team].append(player)

    def move_player(self, player, point):
        self.grid[y(player.point)][x(player.point)] = '.'
        self.grid[y(point)][x(point)] = player.team
        self.players.pop(player.point)
        self.players[point] = player
        # print("{} moves to {}".format(player, point))
        player.point = point

    def remove_player(self, player):
        if self.part2 and player.team == 'E':
            raise ElfDeath()
        self.players.pop(player.point)
        self.teams[player.team].remove(player)
        self.grid[player.point[0]][player.point[1]] = '.'

    def round(self):
        turn_order = list(sorted(self.players.values(), key=lambda p: p.point))
        for player in turn_order:
            if player.hp <= 0:
                # was knocked out this round. No turn
                continue
            player.play(self)

    def calc(self):
        return self.rounds_completed * sum(p.hp for p in self.players.values())

    def play(self, quiet=False):
        if not quiet:
            print(self)
        try:
            while True:
                # print("Round {} Begin: ".format(rounds_completed + 1))
                self.round()
                self.rounds_completed += 1
                # print(self)
        except NoOpponents:
            pass
        if not quiet:
            print(self)
            print("{} rounds completed".format(self.rounds_completed))
            for p in sorted(self.players.values(), key=lambda p: p.point):
                print(p)
            print(self.calc())


def load(input):
    game = Game()
    with open(input, 'r') as f:
        for line in f:
            col = []
            for c in line.strip():
                if c in ('G', 'E'):
                    game.add_player((Player(len(game.grid), len(col), c, 200, 3)))
                col.append(c)
            game.grid.append(col)
    return game


def part1(args):
    game = load(args.input)
    game.play()


def part2(args):
    min_elf_power = 4
    max_elf_power = 40
    solutions = {}
    while True:
        game = load(args.input)
        game.part2 = True
        chosen_elf_power = (max_elf_power + min_elf_power) / 2
        for elf in game.teams['E']:
            elf.ap = chosen_elf_power
        try:
            game.play(True)
            max_elf_power = chosen_elf_power
            print("{}: Elves win with no losses".format(chosen_elf_power))
            solutions[chosen_elf_power] = game.calc()
        except ElfDeath:
            min_elf_power = chosen_elf_power + 1
            print("{}: Elf dies".format(chosen_elf_power))
        if min_elf_power == max_elf_power:
            print("Found optimum power {}".format(min_elf_power))
            print("solution: {}".format(solutions[min_elf_power]))
            break
        if min_elf_power > max_elf_power:
            print("No solution")
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
