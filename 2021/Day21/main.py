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


# All possible outcomes of rolling a 3-sided die 3 times
#  key: Sum of the roll values
#  value: Number of instances of this possible outcome
POSSIBILITIES = Counter([sum(x) for x in itertools.product(list(range(1, 4)), repeat=3)])

# Maps a tuple (position, score) to all possible outcomes from that position
# Outcomes are stored as a mapping. 
#  key: Number of turns to reach a winning score
#  value: Number of instances of this possibility
ScoreMap = {}
WINNING_COUNTER = Counter({0: 1})


def sim1(pos, score):
    if score >= 21:
        # Base case - Once the score has reached 21, the game is over. 0 turns, 1 possibility
        return WINNING_COUNTER
    key = (pos, score)
    # The answer never changes for a given position, just remember and return it
    answer = ScoreMap.get(key, None)
    if answer is not None:
        return answer
    answer = Counter()
    # For each possible roll
    for roll, roll_count in POSSIBILITIES.items():
        # calculate a new position
        new_pos = (pos + roll - 1) % 10 + 1
        # and a new score
        new_score = score + new_pos
        # For each possible outcome at that position and score
        for win_turns, win_count in sim1(new_pos, new_score).items():
            # calculate the number of instances we can get it from here (*roll_count)
            # and increase the number of turns taken to win by 1
            answer[win_turns + 1] += (win_count * roll_count)
    ScoreMap[key] = answer
    return answer


def calc_player_possibilities(start_pos):
    turns_to_win = sim1(start_pos, 0)
    # Number of universes that make it through each round. In the 0th round, there is only 1 universe
    universes_in_turn = [1]
    turns = len(universes_in_turn)
    while universes_in_turn[-1] != 0:
        # number of universes in the previous turn, times the number of new universes created
        # by rolling the dice 3 times (3**3). Subtract out the number of universes that win this turn.
        universes_in_turn.append(universes_in_turn[turns - 1] * (3**3) - turns_to_win[turns])
        turns += 1

    print(sorted(turns_to_win.items()), sum(turns_to_win.values()))
    print(universes_in_turn)

    return turns_to_win, universes_in_turn


def part2(p1, p2):
    p1_rounds, poss1 = calc_player_possibilities(p1)
    p2_rounds, poss2 = calc_player_possibilities(p2)
    
    p1_wins = 0
    p2_wins = 0

    for turns, wins in sorted(p1_rounds.items()):
        # since p1 goes first, it defeats all opponent universes that make it through the previous round
        p1_wins += wins * poss2[turns-1]
    for turns, wins in sorted(p2_rounds.items()):
        # p2 defeats all opponent universes that make it through the same number of rounds
        p2_wins += wins * poss1[turns]
    
    print('p1:', p1_wins)
    print('p2:', p2_wins)


if __name__ == "__main__":
    #part1(4, 8)
    part1(6, 2)
    #part2(sys.argv[1])
    print(POSSIBILITIES)
    part2(4, 8)
    part2(6, 2)
