from collections import deque
import itertools


FILE = "input.txt"
# FILE = "example1.txt"


def read_file(path):
    with open(path, "r") as f:
        decks = []
        for line in f:
            if line.startswith("Player"):
                cur_deck = deque()
                decks.append(cur_deck)
            try:
                cur_deck.append(int(line))
            except:
                pass

        return decks


def combat_round(decks):
    c0 = decks[0].popleft()
    c1 = decks[1].popleft()
    if c0 > c1:
        decks[0].append(c0)
        decks[0].append(c1)
    else:
        decks[1].append(c1)
        decks[1].append(c0)


def calc_score(deck):
    score = 0
    for i, card in enumerate(reversed(deck)):
        score += (i + 1) * card
    return score


def part1():
    decks = read_file(FILE)
    # print(decks)
    while not any(len(d) == 0 for d in decks):
        combat_round(decks)
    if len(decks[0]) > 0:
        print("P1: ", calc_score(decks[0]))
    else:
        print("P2: ", calc_score(decks[1]))


def slice(obj, s, e):
    return obj.__class__(itertools.islice(obj, s, e))


def deck_tuple(decks):
    return tuple(decks[0]), tuple(decks[1])


def rcombat_game(decks):
    round_history = set()
    winner = None
    while winner is None:
        winner = rcombat_round(decks, round_history)
    return winner, decks[winner]


def rcombat_round(decks, round_history):
    # First, does this configuration match a prior configuration in this game
    cur_cfg = deck_tuple(decks)
    if cur_cfg in round_history:
        # Automatic win for Player 1
        return 0
    # print(self.depth, decks)
    round_history.add(cur_cfg)
    cards = decks[0].popleft(), decks[1].popleft()
    if cards[0] <= len(decks[0]) and cards[1] <= len(decks[1]):
        # Play sub-game to determine round winner
        winner, _ = rcombat_game((slice(decks[0], 0, cards[0]), slice(decks[1], 0, cards[1])))
    elif cards[0] > cards[1]:
        winner = 0
    else:
        winner = 1
    loser = int(not winner)
    decks[winner].append(cards[winner])
    decks[winner].append(cards[loser])
    if len(decks[loser]) == 0:
        return winner
    return None


def part2():
    decks = read_file(FILE)
    winner, deck = rcombat_game(decks)
    print(winner, calc_score(deck), deck)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
