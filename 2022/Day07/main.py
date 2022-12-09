#!/usr/bin/env python3
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()

def load(args):
    lines = []
    with open(args.input, 'r') as f:
        for line in f:
            lines.append(line)
    return lines


class TreeNode(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self._size = None
        self.contents = {}
    
    @property
    def size(self):
        if self._size is None:
            if not self.contents:
                self._size = 0
            else:
                self._size = sum(item.size for item in self.contents.values())
        return self._size
    
    def __repr__(self):
        return '{} (dir)'.format(self.name)


class FileNode(object):
    def __init__(self, name, size, parent):
        self.name = name
        self.size = size
        self.parent = parent
    
    def __repr__(self):
        return '{} (file, size={})'.format(self.name, self.size)


class Parser(object):
    def __init__(self):
        self.root = TreeNode('/', None)
        self.pwd = self.root
        
    def cd(self, dirname):
        if dirname == '/':
            return self.root
        if dirname == '..':
            return self.pwd.parent
        if dirname not in self.pwd.contents:
            self.pwd.contents[dirname] = TreeNode(dirname, self.pwd)
        return self.pwd.contents[dirname]

    def ls(self, data, i):
        while i < len(data):
            entry = data[i].split()
            if entry[0] == '$':
                return i
            if entry[0] == 'dir':
                self.cd(entry[1])
            else:
                self.pwd.contents[entry[1]] = FileNode(entry[1], int(entry[0]), self.pwd)
            i += 1
        return i

    def run(self, data):
        i = 0
        while i < len(data):
            components = data[i].split()
            # should be a command
            if components[1] == 'cd':
                self.pwd = self.cd(components[2])
                i += 1
            elif components[1] == 'ls':
                i = self.ls(data, i + 1)


def find_dirs(root, results):
    if root.size <= 100000:
        results.append(root)
    for child in root.contents.values():
        if isinstance(child, TreeNode):
            find_dirs(child, results)
    

def find_dirs2(root, results, thresh):
    if root.size >= thresh:
        results.append(root)
    for child in root.contents.values():
        if isinstance(child, TreeNode):
            find_dirs2(child, results, thresh)


def part1(data):
    p = Parser()
    p.run(data)
    results = []
    find_dirs(p.root, results)
    print(sum(item.size for item in results))


def part2(data):
    p = Parser()
    p.run(data)
    used_space = p.root.size
    free_space = 70000000 - used_space
    needed_space = 30000000 - free_space
    results = []
    find_dirs2(p.root, results, needed_space)
    choose = sorted(results, key=lambda i: i.size)[0]
    print(choose, choose.size)
    


data = load(args)
if not args.part2:
    part1(data)
else:
    part2(data)

