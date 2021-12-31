import sys
from collections import Counter
import itertools


class DeterministicDice(object):
    def __init__(self):
        self.value = 99
        self.count = 0
    
    def roll(self):
        self.count += 1
        self.value = (self.value + 1) % 100
        return 1 + self.value


class DiracDiceGame(object):
    def __init__(self, die, p1, p2):
        self.die = die
        self.scores = [0, 0]
        self.positions = [p1-1, p2-1]
        self.turn = 0
    
    def next_turn(self):
        return (self.turn + 1) & 1

    def take_turn(self):
        value = sum(self.die.roll() for _ in range(3))
        pos = (self.positions[self.turn] + value) % 10
        self.scores[self.turn] += pos + 1
        self.positions[self.turn] = pos
        if self.scores[self.turn] >= 1000:
            raise Exception('Winner!')
        self.turn = self.next_turn()
    
    def play(self):
        try:
            while True:
                self.take_turn()
        except Exception:
            print(self.scores[self.next_turn()], '*', self.die.count, '=', self.scores[self.next_turn()] * self.die.count)


def part1(*args):
     DiracDiceGame(DeterministicDice(), *args).play()


POSSIBILITIES = Counter([sum(x) for x in itertools.product(list(range(1, 4)), repeat=3)])

ScoreMap = {}
WINNING_COUNTER = Counter({0: 1})


def sim1(pos, score):
    if score >= 21:
        return WINNING_COUNTER
    key = (pos, score)
    answer = ScoreMap.get(key, None)
    if answer is not None:
        return answer
    answer = Counter()
    for roll, roll_count in POSSIBILITIES.items():
        new_pos = (pos + roll) % 10
        new_score = score + new_pos + 1
        for win_turns, win_count in sim1(new_pos, new_score).items():
            answer[win_turns+1] += (win_count * roll_count)
    ScoreMap[key] = answer
    return answer


def part2(p1, p2):
    for score in range(21):
        for pos in range(10):
            sim1(pos, score)
    p1_rounds = sim1(p1-1, 0)
    p2_rounds = sim1(p2-1, 0)
    print(sorted(p1_rounds.items()), sum(p1_rounds.values()))
    print(sorted(p2_rounds.items()), sum(p2_rounds.values()))
    p1_wins = 0
    p2_wins = 0
    poss1 = [27**0, 27**1, 27**2]
    poss2 = [27**0, 27**1, 27**2]
    for turns1, wins1 in sorted(p1_rounds.items()):
        poss1.append(poss1[turns1-1] * 27 - wins1)
        #p1_wins += wins1 * (3**(2*turns1-1))
        #for turns2, wins2 in p2_rounds.items():
        #    if turns2 < turns1:
        #        p1_wins -= wins2 * (3**(2*turns2))
    for turns2, wins2 in sorted(p2_rounds.items()):
        poss2.append(poss2[turns2-1] * 27 - wins2)
    print(poss1)
    print(poss2)


if __name__ == "__main__":
    #part1(4, 8)
    part1(6, 2)
    #part2(sys.argv[1])
    print(POSSIBILITIES)
    part2(4, 8)
