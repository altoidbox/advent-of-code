#!/usr/bin/env python3
import argparse
from collections import deque


def load(path):
    with open(path, "r") as f:
        data = f.read().strip()
    return data


def next_free(blocks, idx, end):
    while idx < end and blocks[idx] != -1:
        idx += 1
    return idx


def prev_used(blocks, idx, start):
    while start < idx and blocks[idx] == -1:
        idx -= 1
    return idx


def part1(path):
    blockmap = load(path)
    id = 0
    blocks = []
    free = False
    for size in (int(item) for item in blockmap):
        if free:
            blocks.extend([-1] * size)
        else:
            blocks.extend([id] * size)
            id += 1
        free = not free
    end_idx = prev_used(blocks, len(blocks) - 1, 0)
    idx = next_free(blocks, 0, end_idx)
    while idx < end_idx:
        blocks[idx] = blocks[end_idx]
        blocks[end_idx] = -1
        end_idx = prev_used(blocks, end_idx - 1, idx + 1)
        idx = next_free(blocks, idx + 1, end_idx)
    answer = 0
    for idx, id in enumerate(blocks):
        if id == -1:
            break
        answer += idx * id
    print(answer)


class Block(object):
    def __init__(self, id_, start, size):
        self.id = id_
        self.start = start
        self.size = size
        self.moved = False
    
    def __repr__(self):
        return f"Block({self.id}, {self.start}, {self.size})"

    def __str__(self):
        if self.id == -1:
            return '.'
        return str(self.id)


def first_fit(blocks, size, start):
    i = 0
    while i < len(blocks):
        blk = blocks[i]
        #print(f"Check {blk!r} sz {size} before {start}")
        if blk.start >= start:
            break
        if blk.id == -1 and blk.size >= size:
            return blk
        i = blk.start + blk.size
    return None


def part2(path):
    blockmap = load(path)
    id = 0
    blocks = []
    free = False
    for size in (int(item) for item in blockmap):
        if free:
            blocks.extend([Block(-1, len(blocks), size)] * size)
        else:
            blocks.extend([Block(id, len(blocks), size)] * size)
            id += 1
        free = not free
        #print(f"Create {blocks[-1]!r}")

    #print(''.join(str(blk) for blk in blocks))
    
    end_idx = len(blocks) - 1
    while end_idx > 0:
        #print(blocks)
        blk = blocks[end_idx]
        if blk.id == -1:
            end_idx = blk.start - 1
            #print(f"skip (free) {blk!r}")
            continue
        if blk.moved:
            end_idx = blk.start - 1
            #print(f"skip (moved) {blk!r}")
            continue
        # attempting to move block at end_idx
        rep_block = first_fit(blocks, blk.size, blk.start)
        if rep_block is None:
            blk.moved = True
            end_idx = blk.start - 1
            #print(f"Can't move {blk!r}")
            continue
        #print(f"Moving {blk!r} to {rep_block!r}")
        # found a sequence of blocks we can fit this one into
        # replace it with a new free block
        free_blk = Block(-1, blk.start, blk.size)
        blocks[free_blk.start:free_blk.start + free_blk.size] = [free_blk] * free_blk.size
        # replace the free space with the file blocks
        blocks[rep_block.start:rep_block.start + blk.size] = [blk] * blk.size
        blk.start = rep_block.start
        blk.moved = True
        # update any remaining free space blocks with the new size
        if rep_block.size > blk.size:
            rep_block.size -= blk.size
            rep_block.start += blk.size
        # mark space where file used to be as free
        # Check prev block
        if free_blk.start - 1 >= 0:
            prev = blocks[free_blk.start - 1]
            if prev.id == -1:
                # Coalesce the prev block into the new free block
                free_blk.start = prev.start
                free_blk.size += prev.size
                # replace the prev blocks with updated coalesced block
                blocks[prev.start:prev.start+prev.size] = [free_blk] * prev.size
        if free_blk.start + free_blk.size < len(blocks):
            next_blk = blocks[free_blk.start + free_blk.size]
            if next_blk.id == -1:
                # Extend free block to overtake the next one
                free_blk.size += next_blk.size
                # replace the next blocks with updated coalesced block
                blocks[next_blk.start:next_blk.start+next_blk.size] = [free_blk] * next_blk.size
        end_idx = free_blk.start - 1
        #print(''.join(str(blk) for blk in blocks))

    answer = 0
    idx = 0
    while idx < len(blocks):
        blk = blocks[idx]
        if blk.id == -1:
            idx = blk.start + blk.size
            continue
        answer += idx * blk.id
        idx += 1
    print(answer)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('path')
    args = p.parse_args()

    part1(args.path)
    part2(args.path)
