#!/usr/bin/env python3

import argparse
import re
from itertools import combinations, permutations


def load(path):
    values = {}
    gates = {}
    with open(path, "r") as f:
        for line in f:
            match = re.match(r'(\w+): (0|1)', line)
            if match:
                values[match.group(1)] = int(match.group(2))
                continue
            match = re.match(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)', line)
            if match:
                gates[match.group(4)] = (match.group(2), match.group(1), match.group(3))
                continue
    return values, gates


def solve(values, gates, wire):
    if wire in values:
        return values[wire]
    op, a, b = gates[wire]
    if op == 'AND':
        result = solve(values, gates, a) & solve(values, gates, b)
    elif op == 'OR':
        result = solve(values, gates, a) | solve(values, gates, b)
    elif op == 'XOR':
        result = solve(values, gates, a) ^ solve(values, gates, b)
    values[wire] = result
    return result


def make_num(values, wires):
    num = 0
    for wire in sorted(wires, reverse=True):
        num <<= 1
        num |= values[wire]
    return num


def perform(values, gates):
    values = values.copy()
    for wire in gates:
        if not wire.startswith('z'):
            continue
        solve(values, gates, wire)
    return make_num(values, (wire for wire in gates if wire.startswith('z')))


def part1(path):
    values, gates = load(path)
    print(len(values))
    print(len(gates))
    value = perform(values, gates)
    print(f'{value}')


def count(iterable):
    return sum(1 for _ in iterable)


def find_root_dependencies(gates, wire, deps):
    if wire not in gates:
        deps.add(wire)
        return
    op, i0, i1 = gates[wire]
    
    for input_ in (i0, i1):
        find_root_dependencies(gates, input_, deps)


def define_in_root_terms(gates, wire):
    if wire not in gates:
        return wire
    op, i0, i1 = gates[wire]
    operands = sorted(define_in_root_terms(gates, input_) for input_ in (i0, i1))

    return f'({operands[0]} {op} {operands[1]})'


def check_dependencies(gates):
    for wire in sorted(gates, reverse=True):
        if not wire.startswith('z'):
            continue
        num = int(wire[1:])
        expected = [f'x{n:02d}' for n in range(num + 1)]
        expected.extend([f'y{n:02d}' for n in range(num + 1)])
        deps = set()
        find_root_dependencies(gates, wire, deps)
        diff = deps.difference(expected)
        if diff:
            print(f'{wire}: {", ".join(sorted(diff))}')


def find_dependencies(gates, wire, deps):
    if wire not in gates:
        return
    op, i0, i1 = gates[wire]
    deps.add(wire)
    for input_ in (i0, i1):
        find_dependencies(gates, input_, deps)
    return deps


def swap_vals(d, k1, k2):
    d[k1], d[k2] = d[k2], d[k1]


def print_wires(gates):
    with open('wires.txt', 'w') as f:
        defined = {}
        for wire in gates:
            defined[wire] = define_in_root_terms(gates, wire)
        for wire in sorted(defined, key=defined.get):
            f.write(f'{wire} = {define_in_root_terms(gates, wire)}\n')


def part2(path):
    values, gates = load(path)
    x = make_num(values, (wire for wire in values if wire.startswith('x')))
    y = make_num(values, (wire for wire in values if wire.startswith('y')))
    expected_value = x + y
    value = perform(values, gates)
    print(f'{x:046b}')
    print(f'{y:046b}')
    print(f'{expected_value:046b}')
    print(f'{value:046b}')
    print(f'{(x + y) ^ (value):046b}')
    prev_deps = set()
    # bit 9:
    # x09 AND y09 -> kfp
    # y09 XOR x09 -> hbs
    # bit 18:
    # x18 AND y18 -> z18
    # y18 XOR x18 -> fwt
    # pvk XOR fwt -> dhq
    # pvk AND fwt -> qdb
    # bit 22:
    # bqp OR gkg -> z22
    # x22 AND y22 -> bqp
    # dcm AND dbp -> gkg
    # x22 XOR y22 -> dbp
    # want z22 = dbp XOR dcm
    # dcm XOR dbp -> pdg
    # bit 27:
    # ckj AND bch -> z27
    # y27 XOR x27 -> ckj
    swaps = [('kfp', 'hbs'), ('z18', 'dhq'), ('pdg', 'z22'), ('jcp', 'z27')]
    for swap in swaps:
        swap_vals(gates, *swap)
    if perform(values, gates) == expected_value:
        print('Swaps worked')
        swap_wires = [w for swap in swaps for w in swap]
        print(','.join(sorted(swap_wires)))
        return

    print_wires(gates)
    # We know there are 46 bits
    for bit in range(46):
        wire = f'z{bit:02d}'
        expected = (expected_value >> bit) & 1
        bit_val = solve(values.copy(), gates, wire)
        deps = find_dependencies(gates, wire, set())
        print(f'{wire} = {define_in_root_terms(gates, wire)}')
        if bit_val != expected:
            print(f'{bit}: {bit_val} != {(expected_value >> bit) & 1}')
            candidate_gates = deps - prev_deps
            print(f'new_deps: {candidate_gates}')
            bit_val = solve(values.copy(), gates, wire)

            #for g1, g2 in combinations(candidate_gates, 2):
            #    gates[g1], gates[g2] = gates[g2], gates[g1]
            #    bit_val = solve(values, gates, wire)
            #    if bit_val == expected:
            #        print(f'Possible swap: {g1} <-> {g2}')
            #    gates[g1], gates[g2] = gates[g2], gates[g1]
            break
        prev_deps = deps

    #check_dependencies(gates)
    #value = perform(values, gates)
    #while value != expected_value:
    #    diff = f'{(x + y) ^ (value):b}'
    #    print(f'{diff}')
    #    bad_bit = list(reversed(diff)).index('1')
    #    print(f'{bad_bit}')
    #    break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


if __name__ == '__main__':
    main()
