import argparse
from datetime import datetime
import re

parser = argparse.ArgumentParser()
parser.add_argument("players", type=int)
parser.add_argument("points", type=int)
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class Node:
    def __init__(self, v, prev=None, next=None):
        self.value = v
        self.prev = prev or self
        self.next = next or self

    def __len__(self):
        count = 1
        cur = self.next
        while cur is not self:
            count += 1
            cur = cur.next
        return count

    def __str__(self):
        l = [self.value]
        cur = self.next
        while cur is not self:
            l.append(cur.value)
            cur = cur.next
        return str(l)

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.next = self.prev = None

    def add_after(self, value):
        node = Node(value, prev=self, next=self.next)
        self.next.prev = node
        self.next = node

    def add_before(self, value):
        node = Node(value, prev=self.prev, next=self)
        self.prev.next = node
        self.prev = node


def play(points, players):
    scores = [0] * players
    origin = Node(0)
    cur = origin
    score_idx = 0
    player_idx = 0
    for turn in range(1, points + 1):
        # print("{}: {}".format(turn, origin))
        score_idx += 1
        if score_idx == 23:
            score_idx = 0
        player_idx += 1
        if player_idx == players:
            player_idx = 0
        if score_idx == 0:
            # score
            scores[player_idx] += turn
            for _ in range(7):
                cur = cur.prev
            node = cur
            cur = node.next
            node.remove()
            scores[player_idx] += node.value
            # print("{} + {} for {}".format(turn, node.value, player_idx))
        else:
            cur = cur.next
            cur.add_after(turn)
            cur = cur.next
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