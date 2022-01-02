from os import stat
import sys
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
COSTS = [1, 10, 100, 1000]
DEBUG = False


def set_debug(value):
    global DEBUG
    DEBUG = value


def debug_print(*msg):
    if not DEBUG:
        return
    print(*msg)


def apod_to_str(apod):
    if apod is None:
        return '.'
    return chr(ord('A') + apod)

def str_to_apod(apod_str):
    if apod_str == '.':
        return None
    return ord(apod_str) - ord('A')


ROOM_SIZE = 4


class Burrow():
    def __init__(self, hallway=None, rooms=None):
        if hallway is None:
            self.hallway = [None] * 11
        else:
            self.hallway = list(hallway)

        self.rooms = []
        for i in range(4):
            if rooms is None:
                self.rooms[i] = []
            else:
                self.rooms.append(list(rooms[i]))

    def items(self, only_top=False):
        for x, apod in enumerate(self.hallway):
            if apod is not None:
                yield Point(x, 0), apod
        for color, room in enumerate(self.rooms):
            x = self.roomx(color)
            size = len(room)
            for i, apod in enumerate(reversed(room)):
                y = i + (ROOM_SIZE - size) + 1
                yield Point(x, y), apod
                # yield only the top entry in the room
                if only_top:
                    break
    
    def keys(self):
        for key, _ in self.items():
            yield key

    def xcolor(self, x):
        return (x//2 - 1)

    def roomx(self, color):
        return (color + 1) * 2
    
    def roomy(self, idx):
        return (ROOM_SIZE - idx)
    
    def room(self, color, slot):
        try:
            return self.rooms[color][ROOM_SIZE - slot - 1]
        except IndexError:
            return None
    
    def getxy(self, x, y):
        if y == 0:
            return self.hallway[x]
        return self.room(self.xcolor(x), y - 1)

    def popxy(self, x, y):
        if y == 0:
            value = self.hallway[x]
            self.hallway[x] = None
        else:
            color = self.xcolor(x)
            # Could validate that the y matches what we expect
            value = self.rooms[color].pop()
        return value
    
    def setxy(self, x, y, value):
        if y == 0:
            self.hallway[x] = value
        else:
            color = self.xcolor(x)
            # Could validate that the y matches what we expect
            self.rooms[color].append(value)

    def can_enter(self, color):
        room = self.rooms[color]
        if len(room) == ROOM_SIZE:
            # room full
            return 0
        for apod in room:
            if apod != color:
                # wrong color in room, cannot enter
                return 0
        # Can enter. space available will also be the new open y value
        return ROOM_SIZE - len(room)
    
    def can_exit(self, color, point):
        # we now assume this will only check the top-most apod in a room
        if point.x != self.roomx(color):
            # Yes, in wrong room. Of course leave
            return True

        # in right room, see if everything below is also right color
        for apod in self.rooms[color]:
            if apod != color:
                return True
        # don't leave. We are in a good spot
        return False
    
    def can_stop(self, x):
        return (x & 1) == 1 or x == 0 or x == 10
    
    def is_solved(self):
        for color, room in enumerate(self.rooms):
            if len(room) != ROOM_SIZE:
                return False
            for apod in room:
                if apod != color:
                    return False
        return True

    def move(self, from_loc, to_loc):
        burrow = Burrow(self.hallway, self.rooms)
        burrow.setxy(to_loc.x, to_loc.y, burrow.popxy(from_loc.x, from_loc.y))
        return burrow

    def __setitem__(self, point, value):
        self.setxy(point.x, point.y, value)

    def __getitem__(self, point):
        return self.getxy(point.x, point.y)
    
    def __str__(self):
        lines = []
        lines.append('#' * (len(self.hallway) + 2))
        lines.append('#{}#'.format(''.join(apod_to_str(apod) for apod in self.hallway)))
        lines.append('###')
        for _ in range(ROOM_SIZE):
            lines.append('  #')
        for color in range(4):
            for slot in range(ROOM_SIZE):
                lines[slot - ROOM_SIZE - 1] += apod_to_str(self.room(color, slot)) + '#'
            lines[-1] += '##'
        lines[-ROOM_SIZE - 1] += '##'
        return '\n'.join(lines)

    @staticmethod
    def from_str(data):
        lines = data.splitlines()
        hallway = [str_to_apod(c) for c in lines[1][1:-1]]
        rooms = []
        for color in range(4):
            room = ''
            idx = (color * 2) + 3
            for slot in range(ROOM_SIZE):
                room += lines[2 + slot][idx]
            room = [str_to_apod(c) for c in reversed(room)]
            rooms.append(room)
        return Burrow(hallway, rooms)
        

def calc_moves(loc, burrow):
    moves = []
    result = [moves, False]
    color = burrow[loc]
    move_cost = COSTS[color]
    cost = 0
    room_x = burrow.roomx(color)
    x, y = loc
    if y == 0:
        # Must move into burrow from hallway. 1 possible move
        # First see if room is blocked
        room_y = burrow.can_enter(color)
        if room_y == 0:
            # blocked!
            return result
        # Then try to find path to the room entrance
        move_dir = 1 if x < room_x else -1
        while x != room_x:
            x += move_dir
            cost += move_cost
            if burrow.hallway[x] is not None:
                # blocked!
                return result

        cost += room_y * move_cost
        moves.append((cost, loc, Point(room_x, room_y)))
        result[1] = True
        return result
    # We are in a burrow, we must move out into the hallway
    if not burrow.can_exit(color, loc):
        return result
    # cost to get to hallway
    cost = y * move_cost
    cur_cost = cost
    # Try each direction
    for move_x in range(x+1, len(burrow.hallway)):
        cur_cost += move_cost
        if burrow.hallway[move_x] is not None:
            # exhausted all moves this direction
            break
        if not burrow.can_stop(move_x):
            continue
        moves.append((cur_cost, loc, Point(move_x, 0)))

    cur_cost = cost
    for move_x in reversed(range(x)):
        cur_cost += move_cost
        if burrow.hallway[move_x] is not None:
            # exhausted all moves this direction
            break
        if not burrow.can_stop(move_x):
            continue
        moves.append((cur_cost, loc, Point(move_x, 0)))
    return result


def all_moves(burrow):
    moves = []
    for loc, apod in burrow.items(only_top=True):
        loc_moves, prioritize = calc_moves(loc, burrow)
        if prioritize:
            return loc_moves
        moves.extend(loc_moves)
        #print(loc, apod, burrow[loc])
    moves.sort()
    return moves

best = None
best_solution = 2**31


def solve(cost, stack):
    global best_solution, best
    if cost >= best_solution:
        return

    burrow = stack[-1]

    if len(stack) > ROOM_SIZE * 4 * 2 + 1:
        print('stack too deep!')
        exit()

    #print(depth)
    #print(burrow)
    
    moves = all_moves(burrow)
    
    # Check for solution if no possible moves
    if len(moves) == 0:
        if burrow.is_solved():
            best_solution = cost
            best = list(stack)
            print(cost)
        return

    for move_cost, from_loc, to_loc in moves:
        stack.append(burrow.move(from_loc, to_loc))
        solve(cost + move_cost, stack)
        stack.pop()


def read_file(fname):
    with open(fname, 'r') as f:
        data = f.read()
    lines = data.splitlines()
    if ROOM_SIZE == 4:
        extra = [
            '  #D#C#B#A#  ',
            '  #D#B#A#C#  '
        ]
        lines = lines[:3] + extra + lines[3:]
    return '\n'.join(lines)


def part1(fname):
    global ROOM_SIZE
    ROOM_SIZE = 2
    burrow = Burrow.from_str(read_file(fname))
    print(burrow)
    solve(0, [burrow])
    for b in best:
        print(b)
    print(best_solution)


def part2(fname):
    data = read_file(fname)
    burrow = Burrow.from_str(data)
    solve(0, [burrow])
    for b in best:
        print(b)
    print(best_solution)


if __name__ == "__main__":
    part2(sys.argv[1])
