import sys
from collections import Counter


def read_file(path):
    g = Graph()
    with open(path, "r") as f:
        for line in f:
            g.add_edge(*line.strip().split('-'))
    return g


def is_small(cave):
    return cave[0].islower()


class Graph(object):
    def __init__(self):
        self.edges = {}
        self.paths = 0
    
    def add_edge(self, edge1, edge2):
        self.edges.setdefault(edge1, set()).add(edge2)
        self.edges.setdefault(edge2, set()).add(edge1)

    def dfs(self):
        self.dfs_node('start', Counter(), [], True)

    def dfs_part2(self):
        self.dfs_node('start', Counter(), [], False)

    def dfs_node(self, root, visited, path, doubled):
        if root == 'end':
            #print(','.join(path + [root]))
            self.paths += 1
            return
        if is_small(root):
            if visited[root] > 0:
                if (doubled or root == 'start'):
                    return
                doubled = True
        visited[root] += 1
        path.append(root)
        for child in self.edges[root]:
            self.dfs_node(child, visited, path, doubled)
        path.pop()
        visited[root] -= 1


def part1(fname):
    g = read_file(fname)
    g.dfs()
    print(g.paths)


def part2(fname):
    g = read_file(fname)
    g.dfs_part2()
    print(g.paths)

if __name__ == "__main__":
    part1(sys.argv[1])
    part2(sys.argv[1])
