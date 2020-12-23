import time


EXAMPLE = "389125467"
INPUT = "583976241"


class Node(object):
    """
    Implements a circular linked list
    """
    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self

    def unlink(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.next = self.prev = self

    def node_at(self, index):
        c = self
        if index > 0:
            while index:
                c = c.next
                index -= 1
        elif index < 0:
            while index:
                c = c.prev
                index += 1
        return c

    def sub_chain(self, start_index, count):
        new_start = self.node_at(start_index)
        new_end = new_start.node_at(count - 1)
        new_start.prev.next = new_end.next
        new_end.next.prev = new_start.prev
        new_start.prev = new_end
        new_end.next = new_start
        return new_start

    def append(self, node):
        self.next.prev = node.prev
        node.prev.next = self.next
        node.prev = self
        self.next = node

    def append_before(self, node):
        self.prev.append(node)

    def each_node(self):
        cur = self
        while True:
            yield cur
            cur = cur.next
            if cur is self:
                break

    def __iter__(self):
        for node in self.each_node():
            yield node.value

    def __getitem__(self, idx):
        n = self.node_at(idx)
        return n.value

    def __contains__(self, value):
        for v in self:
            if v == value:
                return True
        return False

    def find(self, value):
        for node in self.each_node():
            if node.value == value:
                return node
        return None

    def __str__(self):
        return "[{}]".format(", ".join(map(str, self)))


def make_nodes(iterable):
    first = None
    for i in iterable:
        n = Node(i)
        if first:
            first.append_before(n)
        else:
            first = n
    return first


def crab_move(chain, max_val):
    picked_up = chain.sub_chain(1, 3)
    destination = chain.value
    while True:
        destination -= 1
        if destination < 1:
            destination = max_val
        if destination not in picked_up:
            break
    chain.find(destination).append(picked_up)
    return chain.next


def example1():
    chain = make_nodes(map(int, EXAMPLE))
    max_val = max(chain)
    print(chain)
    for _ in range(10):
        chain = crab_move(chain, max_val)
    print(chain)
    for _ in range(90):
        chain = crab_move(chain, max_val)
    print("".join(map(str, chain.find(1))))


def part1():
    chain = make_nodes(map(int, INPUT))
    max_val = max(chain)
    print(chain)
    for _ in range(100):
        chain = crab_move(chain, max_val)
    print("".join(map(str, chain.find(1))))


def efficient_crab_move(chain, max_val, node_map):
    picked_up = chain.sub_chain(1, 3)
    destination = chain.value
    while True:
        destination -= 1
        if destination < 1:
            destination = max_val
        if destination not in picked_up:
            break
    node_map[destination].append(picked_up)
    return chain.next


def part2():
    # chain = make_nodes(map(int, EXAMPLE))
    chain = make_nodes(map(int, INPUT))
    node_list = [0]
    for value in range(1, 10):
        node_list.append(chain.find(value))
    for value in range(10, 1000000 + 1):
        chain.append_before(Node(value))
        node_list.append(chain.prev)
    max_val = 1000000
    start = time.time()
    for _ in range(10000000):
        chain = efficient_crab_move(chain, max_val, node_list)
    print("{} s".format(time.time() - start))
    node1 = node_list[1]
    print(node1[1], node1[2], node1[1] * node1[2])


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
