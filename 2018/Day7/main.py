import argparse
import re
from collections import OrderedDict
import heapq


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class Node(object):
    def __init__(self, name):
        self.name = name
        self.dependencies = set()
        self.dependents = set()
        self.worker = None
        self.work_time = None

    def walk(self, func, *args, **kwargs):
        func(self, *args, **kwargs)
        #for child in self.children:
        #    child.walk(func, *args, **kwargs)


def read_input(path):
    nodes = {}
    with open(path, "r") as f:
        for line in f:
            dependency, step = re.match(r'Step (\w) must be finished before step (\w) can begin\.', line).groups()
            step_node = nodes.get(step, None)
            if not step_node:
                step_node = Node(step)
                nodes[step] = step_node
            dep_node = nodes.get(dependency)
            if not dep_node:
                dep_node = Node(dependency)
                nodes[dependency] = dep_node
            step_node.dependencies.add(dependency)
            dep_node.dependents.add(step)
    return nodes


def part1(args):
    nodes = read_input(args.input)
    answer = ''

    ready = []
    for item in nodes.values():
        if len(item.dependencies) == 0:
            heapq.heappush(ready, item.name)

    while len(ready):
        item = heapq.heappop(ready)
        answer += item
        for dep in nodes[item].dependents:
            dep_node = nodes[dep]
            dep_node.dependencies.remove(item)
            if len(dep_node.dependencies) == 0:
                heapq.heappush(ready, dep)

    print(answer)


def work(nodes, base_time, num_workers):
    ready = []
    for item in nodes.values():
        if len(item.dependencies) == 0:
            heapq.heappush(ready, item.name)

    worker_pool = set(range(num_workers))
    work_list = []
    time = 0
    completed = ''
    while len(ready) or len(work_list):
        remove_list = []
        for item in work_list:
            item.work_time -= 1
            if item.work_time == 0:
                completed += item.name
                for dep in item.dependents:
                    dep_node = nodes[dep]
                    dep_node.dependencies.remove(item.name)
                    if len(dep_node.dependencies) == 0:
                        heapq.heappush(ready, dep)
                remove_list.append(item)
        for item in remove_list:
            work_list.remove(item)
            worker_pool.add(item.worker)
        while len(worker_pool) and len(ready):
            item = nodes[heapq.heappop(ready)]
            item.worker = worker_pool.pop()
            item.work_time = base_time + (1 + ord(item.name) - ord('A'))
            work_list.append(item)
        print("{}: {}".format(time, completed))
        time += 1
    print(completed)
    return time - 1


def part2(args):
    nodes = read_input(args.input)

    if 'test' in args.input:
        answer = work(nodes, 0, 2)
    else:
        answer = work(nodes, 60, 5)

    print("{}".format(answer))


if args.part2:
    part2(args)
else:
    part1(args)
