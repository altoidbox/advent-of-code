def read_file(path):
    with open(path, "r") as f:
        numbers = list(map(int, f.readline().split(',')))
        boards = []
        board = None
        for line in f:
            line = line.strip()
            if not line:
                board = []
                boards.append(board)
                continue
            board.append(list(map(int, line.split())))

    return numbers, boards


class Point(object):
    def __self__(self, x, y):
        self.x = x
        self.y = y
        self.on = False


class Board(object):
    def __init__(self, grid):
        self.dict = {}
        self.value = 0
        self.columns = [0] * len(grid[0])
        self.rows = [0] * len(grid)
        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                self.dict[val] = (x, y)
                self.value += val
        self.score = 0
    
    def select(self, number):
        point = self.dict.get(number)
        if not point:
            return
        x, y = point
        self.value -= number
        self.columns[x] += 1
        self.rows[y] += 1
        if self.columns[x] == len(self.columns) or self.rows[y] == len(self.rows):
            self.score = self.value * number


def part1():
    numbers, boards = read_file('input.txt')
    #print(numbers, boards)
    boards = [Board(b) for b in boards]
    for n in numbers:
        for b in boards:
            b.select(n)
            if b.score:
                print(b.score)
                return


def part2():
    numbers, boards = read_file('input.txt')
    #print(numbers, boards)
    boards = [Board(b) for b in boards]
    for n in numbers:
        for b in boards:
            b.select(n)
            if b.score:
                print(b.score)
        boards = list(filter(lambda b: b.score == 0, boards))


def main():
    #part1()
    part2()


if __name__ == "__main__":
    main()
