#!/usr/bin/env python3
import argparse
import re
import heapq
from itertools import combinations, permutations

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def load(path):
    graph = {}
    rates = {}
    with open(args.input, "r") as f:
        for line in f:
            m = re.match(r'Valve (\w+) .+ rate=(\d+); .+valves? (.+)', line)
            name, rate, edges = m.groups()
            graph[name] = edges.split(', ')
            rates[name] = int(rate)
    return graph, rates
        

def dijkstra(g, start):
    inf = float('inf')
    dist = 1  #  all costs are 1 in this problem
    visited = set()
    costs = { start: 0 }
    path = { start: None }
    to_visit = [(0, start)]
    heapq.heapify(to_visit)

    while len(to_visit) > 0:
        path_cost, source = heapq.heappop(to_visit)
        visited.add(source)
        for neighbor in g[source]:
            if neighbor in visited:
                continue
            new_cost = costs[source] + dist
            old_cost = costs.get(neighbor, inf)
            if new_cost < old_cost:
                heapq.heappush(to_visit, (new_cost, neighbor))
                costs[neighbor] = new_cost
                path[neighbor] = source

    # return the path cost of the best path to the destination
    # if we wanted the actual path, we would walk path nodes from the dest to the source
    return costs


class part1(object):
    def __init__(self, data):
        self.graph, self.rates = data
        self.costs = {}
        self.time = 30
        self.pressure = 0
        self.rate = 0
        #self.run()
        print(self.runwith('AA', set(loc for loc in self.rates.keys() if self.rates[loc] > 0), 30, 0, 0, []))

    def path_costs(self, start):
        pc = self.costs.get(start, None)
        if pc is None:
            pc = dijkstra(self.graph, start)
            self.costs[start] = pc
        return pc

    def runwith(self, loc, valves, time, rate, pressure, path):
        if len(valves) == 0 or time == 0:
            return pressure + rate * time, list(path)
        pc = self.path_costs(loc)
        best = 0
        best_path = []
        for dest in list(valves):
            valves.discard(dest)
            passed = pc[dest] + 1
            if time - passed < 0:
                passed = time
            path.append(dest)
            result, cpath = self.runwith(dest, valves, time - passed, rate + self.rates[dest], pressure + rate * passed, path)
            if result > best:
                best = result
                best_path = cpath
            path.pop()
            valves.add(dest)
        return best, best_path

    def run(self):
        location = 'AA'
        valves = set(loc for loc in self.rates.keys() if self.rates[loc] > 0)
        print(valves)
        while self.time:
            valves.discard(location)
            pc = self.path_costs(location)
            best_value = 0
            best_dest = None
            for dest in valves:
                cost = pc[dest]
                value = (self.time - cost - 1) * self.rates[dest]
                if value > best_value:
                    best_value = value
                    best_dest = dest
                    print('best-', dest, cost, value)
                elif value == best_value:
                    print('double best', dest, best_dest, value, cost)
            if not best_dest:
                print('no best')
                break
            print(pc[best_dest], best_dest, self.rates[best_dest], best_value)
            time_passed = pc[best_dest] + 1
            self.pressure += self.rate * time_passed
            self.rate += self.rates[best_dest]
            self.time -= time_passed
            location = best_dest
            print(self.time, self.rate, self.pressure)
        self.pressure += self.rate * self.time
        print(self.time, self.rate, self.pressure)


def swap(a, b):
    return b, a


class part2(object):
    def __init__(self, data):
        self.graph, self.rates = data
        self.costs = {}
        print(self.runwith('AA', 0, [], 'AA', 0, [], set(loc for loc in self.rates.keys() if self.rates[loc] > 0), 26, 0, 0))

    def path_costs(self, start):
        pc = self.costs.get(start, None)
        if pc is None:
            pc = dijkstra(self.graph, start)
            self.costs[start] = pc
        return pc

    def runwith(self, l1, l1t, p1, l2, l2t, p2, valves, time, rate, pressure):
        if len(valves) == 0 or time == 0:
            passed, dest = max((l1t, l1), (l2t, l2))
            passed = min(passed, time)
            if passed != 0:
                increase = self.rates[dest]
                if l1t == l2t:
                    increase = self.rates[l1] + self.rates[l2]
                pressure += rate * passed
                rate += increase
                time -= passed
            return pressure + rate * time, (list(p1), list(p2))
        
        best = 0
        best_path = []
        if l1t == 0 and l2t == 0:
            pc1 = self.path_costs(l1)
            pc2 = self.path_costs(l2)
            if l1 == l2:
                # if they're in the same spot, who goes were doesn't matter, so (a, b) and (b, a) is identical
                possibilities = combinations(list(valves), 2)
            else:
                # who goes where *does* matter, if they aren't at the same spot
                possibilities = permutations(list(valves), 2)
            for d1, d2 in possibilities:
                valves.discard(d1)
                valves.discard(d2)
                d1t = pc1[d1] + 1
                d2t = pc2[d2] + 1
                p1.append(d1)
                p2.append(d2)
                passed, dest = min((d1t, d1), (d2t, d2))
                increase = self.rates[dest]
                if d1t == d2t:
                    increase = self.rates[d1] + self.rates[d2]
                passed = min(passed, time)
                # do it recursively
                result, cpath = self.runwith(d1, d1t - passed, p1, d2, d2t - passed, p2, valves, time - passed, rate + increase, pressure + rate * passed)
                if result > best:
                    best = result
                    best_path = cpath
                p2.pop()
                p1.pop()
                valves.add(d2)
                valves.add(d1)
        else:
            if l2t == 0:
                (l1, l1t, p1), (l2, l2t, p2) = swap((l1, l1t, p1), (l2, l2t, p2))
            pc = self.path_costs(l1)
            for d1 in list(valves):
                valves.discard(d1)
                d1t = pc[d1] + 1
                passed, dest = min((d1t, d1), (l2t, l2))
                increase = self.rates[dest]
                if d1t == l2t:
                    increase = self.rates[d1] + self.rates[l2]
                passed = min(passed, time)
                p1.append(d1)
                result, cpath = self.runwith(d1, d1t - passed, p1, l2, l2t - passed, p2, valves, time - passed, rate + increase, pressure + rate * passed)
                if result > best:
                    best = result
                    best_path = cpath
                p1.pop()
                valves.add(d1)
        return best, best_path


data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

