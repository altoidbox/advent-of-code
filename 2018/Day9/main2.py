import argparse
from datetime import datetime
import re
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument("players", type=int)
parser.add_argument("points", type=int)
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def play(points, players):
    scores = [0] * players
    cur = deque()
    cur.append(0)
    score_idx = 0
    player_idx = 0
    for turn in range(1, points + 1):
        # print("{}: {}".format(turn - 1, cur))
        score_idx += 1
        if score_idx == 23:
            score_idx = 0
        player_idx += 1
        if player_idx == players:
            player_idx = 0
        if score_idx == 0:
            # score
            scores[player_idx] += turn
            cur.rotate(7)
            scores[player_idx] += cur.popleft()
            # print("{} + {} for {}".format(turn, node.value, player_idx))
        else:
            cur.rotate(-2)
            cur.appendleft(turn)
    return scores


def part1(args):
    scores = play(args.points, args.players)
    print(scores)
    print(max(scores))


def part2(args):
    pass


if args.part2:
    part2(args)
else:
    part1(args)


#476 players; last marble is worth 71431 points
# 10 players; last marble is worth 1618 points: high score is 8317
# 13 players; last marble is worth 7999 points: high score is 146373
# 17 players; last marble is worth 1104 points: high score is 2764
# 21 players; last marble is worth 6111 points: high score is 54718
# 30 players; last marble is worth 5807 points: high score is 37305
# 9, 25 = 32