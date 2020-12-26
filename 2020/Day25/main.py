from collections import defaultdict


def read_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
        cp = int(lines[0])
        dp = int(lines[1])
    return cp, dp


def find_loopcount(subj, target):
    cur = 1
    loop_count = 0
    while cur != target:
        cur = (cur * subj) % 20201227
        loop_count += 1
    return loop_count


def transform(subj, loopcount):
    cur = 1
    for _ in range(loopcount):
        cur = (cur * subj) % 20201227
    return cur


def part1(path):
    card_pubkey, door_pubkey = read_file(path)
    card_loopcount = find_loopcount(7, card_pubkey)
    door_loopcount = find_loopcount(7, door_pubkey)
    print(card_loopcount, door_loopcount)
    card_enc = transform(door_pubkey, card_loopcount)
    door_enc = transform(card_pubkey, door_loopcount)
    print(card_enc, door_enc)


def main():
    part1("example.txt")
    part1("input.txt")


if __name__ == "__main__":
    main()
