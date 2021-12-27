import sys
import itertools


def read_file(path):
    with open(path, "r") as f:
        return [s.strip() for s in f]


class SFNum(object):
    def __init__(self, value, parent=None):
        if isinstance(value, list):
            for child in value:
                child.parent = self
        self.value = value
        self.parent = parent
        self.visited = False

    def isparent(self):
        return isinstance(self.value, list)
    
    @property
    def left(self):
        return self.value[0]
    
    @property
    def right(self):
        return self.value[1]

    @staticmethod
    def _parse(line, i):
        if line[i] != '[':
            # Regular number
            return SFNum(int(line[i])), i + 1
        # else Pair
        left, i = SFNum._parse(line, i + 1)
        if line[i] != ',':
            raise Exception("Expected ','")
        right, i = SFNum._parse(line, i + 1)
        if line[i] != ']':
            raise Exception("Expected ']'")
        return SFNum([left, right]), i + 1

    @staticmethod
    def parse(line):
        return SFNum._parse(line, 0)[0]

    def first(self):
        node = self
        while node.isparent():
            node = node.left
        return node

    def next(self):
        if self.isparent():
            return self.right.first()
        node = self
        while node.parent:
            if node.parent.right is node:
                node = node.parent
            else:
                return node.parent
        return None
    
    def last(self):
        node = self
        while node.isparent():
            node = node.right
        return node

    def prev(self):
        if self.isparent():
            return self.left.last()
        node = self
        while node.parent:
            if node.parent.left is node:
                node = node.parent
            else:
                return node.parent
        return None

    def prevval(self):
        cur = self.prev()
        while cur:
            if not cur.isparent():
                return cur
            cur = cur.prev()
        return None
    
    def nextval(self):
        cur = self.next()
        while cur:
            if not cur.isparent():
                return cur
            cur = cur.next()
        return None

    def walk(self, depth, func):
        if self.isparent():
            result = self.left.walk(depth + 1, func)
            if result is not None:
                return result

            result = func(self, depth)
            if result is not None:
                return result

            return self.right.walk(depth + 1, func)
        else:
            return func(self, depth)

    def explode(self):
        #print('e', self)
        p = self.left.prevval()
        if p:
            #print('p', p)
            p.value += self.left.value
        n = self.right.nextval()
        if n:
            #print('n', n)
            n.value += self.right.value
        self.value = 0

    def split(self):
        newval = [
            SFNum(self.value // 2, parent=self),
            SFNum(self.value // 2 + self.value % 2, parent=self),
        ]
        #print('s', self, newval)
        self.value = newval

    def reduce(self):
        while True:
            #print(self)
            exp = self.walk(0, find_to_explode_callback)
            if exp:
                exp.explode()
                continue
            spl = self.walk(0, find_to_split_callback)
            if spl:
                spl.split()
                continue
            break

    def magnitude(self):
        if self.isparent():
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()
        return self.value

    def __hash__(self):
        return hash(self.tuple)

    def dup(self):
        if self.isparent():
            return SFNum([child.dup() for child in self.value])
        return SFNum(self.value)

    def __add__(self, other):
        newval = SFNum([self.dup(), other.dup()])
        newval.reduce()
        return newval

    def __str__(self):
        if self.isparent():
            return '[{}]'.format(','.join(str(v) for v in self.value))
        return str(self.value)

    def __repr__(self):
        return str(self)


def find_to_explode_callback(node, depth):
    if node.isparent() and depth >= 4:
        return node
    return None


def find_to_split_callback(node, depth):
    if not node.isparent() and node.value >= 10:
        return node
    return None


def part1():
    pass


def part2():
    pass


parse_samples = [
    '[1,2]',
    '[[1,2],3]',
    '[9,[8,7]]',
    '[[[[1,2],[3,4]],[[5,6],[7,8]]],9]',
    '[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]',
    '[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]',
]
def test_parse():
    for s in parse_samples:
        num = SFNum.parse(s)
        print(num)


explode_samples = [
    '[[[[[9,8],1],2],3],4]',
    '[7,[6,[5,[4,[3,2]]]]]',
    '[[6,[5,[4,[3,2]]]],1]',
    '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
    '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'
]
def test_explode():
    for s in explode_samples:
        num = SFNum.parse(s)
        print(num)
        num.reduce()
        print(num)


add_samples = [
    ['[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]'],
    ['[1,1]','[2,2]','[3,3]','[4,4]'],
    ['[1,1]','[2,2]','[3,3]','[4,4]','[5,5]'],
    ['[1,1]','[2,2]','[3,3]','[4,4]','[5,5]','[6,6]'],
]
def test_add():
    for lst in add_samples:
        sum_list(lst)


def sum_list(lst):
    result = SFNum.parse(lst[0])
    for item in lst[1:]:
        result += SFNum.parse(item)
    print(result.magnitude(), result)
    return result


def part1():
    sum_list(read_file(sys.argv[1]))


def part2():
    nums = [SFNum.parse(x) for x in read_file(sys.argv[1])]
    print(max((a + b).magnitude() for a, b in itertools.permutations(nums, 2)))


if __name__ == '__main__':
    #part1()
    part2()
