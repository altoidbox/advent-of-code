from collections import deque


def read_file(path):
    buckets = deque()
    for i in range(9):
        buckets.append(0)

    with open(path, "r") as f:
        for i in map(int, f.readline().split(',')):
            buckets[i] += 1
        
    return buckets


def part1(count):
    buckets = read_file('input.txt')
    for _ in range(count):
        n = buckets.popleft()
        buckets.append(n)
        buckets[6] += n
    print(sum(buckets))


def main():
    part1(80)
    part1(256)


if __name__ == "__main__":
    main()
