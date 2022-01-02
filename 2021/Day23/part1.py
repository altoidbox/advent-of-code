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


class Burrow():
    def __init__(self, hallway=None, rooms=None):
        if hallway is None:
            self.hallway = [None] * 11
        else:
            self.hallway = list(hallway)
        if rooms is None:
            self.rooms = [None] * 8
        else:
            self.rooms = list(rooms)

    def items(self):
        for x, apod in enumerate(self.hallway):
            if apod is not None:
                yield Point(x, 0), apod
        for i, apod in enumerate(self.rooms):
            if apod is not None:
                yield Point((i//2 + 1) * 2, (i & 1) + 1), apod
    
    def keys(self):
        for key, _ in self.items():
            yield key

    def roomx(self, color):
        return (color + 1) * 2
    
    def roomidx(self, color, slot):
        return color*2 + slot

    def room(self, color, slot):
        return self.rooms[color*2 + slot]
    
    def getxy(self, x, y):
        if y == 0:
            return self.hallway[x]
        return self.rooms[(x//2 - 1) * 2 + y - 1]

    def popxy(self, x, y):
        if y == 0:
            value = self.hallway[x]
            self.hallway[x] = None
        else:
            idx = (x//2 - 1) * 2 + y - 1
            value = self.rooms[idx]
            self.rooms[idx] = None
        return value
    
    def setxy(self, x, y, value):
        if y == 0:
            self.hallway[x] = value
        else:
            self.rooms[(x//2 - 1) * 2 + y - 1] = value

    def can_enter(self, color):
        i = self.roomidx(color, 0)
        if self.rooms[i] is not None:
            return 0
        other = self.rooms[i+1]
        if other == color:
            return 1
        elif other is None:
            return 2
        return 0
    
    def can_exit(self, color, point):
        room_x = self.roomx(color)
        if point.y == 1:
            if point.x == room_x and self.room(color, 1) == color:
                # in right room with right partner
                return 0
            return 1
        if point.y == 2:
            if point.x == room_x:
                # in right room
                return 0
            if self.getxy(point.x, 1) is not None:
                # blocked
                return 0
            return 2
        raise Exception("Illegal can_exit check!")
    
    def can_stop(self, x):
        return (x & 1) == 1 or x == 0 or x == 10
    
    def is_solved(self):
        for i, apod in enumerate(self.rooms):
            if apod is None:
                return False
            if i//2 != apod:
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
        lines.append('  #')
        lines.append('  #')
        for color in range(4):
            lines[-3] += apod_to_str(self.rooms[color*2]) + '#'
            lines[-2] += apod_to_str(self.rooms[color*2+1]) + '#'
            lines[-1] += '##'
        lines[-3] += '#'
        return '\n'.join(lines)

    @staticmethod
    def from_str(data):
        lines = data.splitlines()
        hallway = [str_to_apod(c) for c in lines[1][1:-1]]
        rooms = ''
        for color in range(4):
            idx = (color * 2) + 3
            rooms += lines[2][idx]
            rooms += lines[3][idx]
        rooms = [str_to_apod(c) for c in rooms]
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
    if burrow.can_exit(color, loc) == 0:
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
    for loc, apod in burrow.items():
        loc_moves, prioritize = calc_moves(loc, burrow)
        if prioritize:
            return loc_moves
        moves.extend(loc_moves)
        #print(loc, apod, burrow[loc])
    moves.sort()
    return moves


best_solution = 2**31


def solve(cost, stack):
    global best_solution
    if cost >= best_solution:
        return

    if len(stack) > 17:
        exit()

    burrow = stack[-1]
    #print(depth)
    #print(burrow)
    
    moves = all_moves(burrow)
    
    # Check for solution if no possible moves
    if len(moves) == 0:
        if burrow.is_solved():
            best_solution = cost
            print(cost)
            for b in stack:
                print(b)
        return

    for move_cost, from_loc, to_loc in moves:
        stack.append(burrow.move(from_loc, to_loc))
        solve(cost + move_cost, stack)
        stack.pop()


def read_file(fname):
    with open(fname, 'r') as f:
        return f.read()


def part1(fname):
    burrow = Burrow.from_str(read_file(fname))
    print(burrow)
    solve(0, [burrow])
    print(best_solution)


if __name__ == "__main__":
    #b = Burrow.from_str(data)
    #print(b)
    #print(all_moves(b))
    part1(sys.argv[1])
