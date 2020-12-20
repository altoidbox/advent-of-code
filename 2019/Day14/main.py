import re
from collections import OrderedDict, defaultdict


def read_file(path):
    maps = {}
    with open(path, "r") as f:
        for line in f:
            sources, produces = line.split("=>")
            consumes = []
            for s in sources.split(','):
                count, rsc = re.match(r'^(\d+) (\w+)$', s.strip()).groups()
                consumes.append((int(count), rsc))
            count, rsc = re.match(r'^(\d+) (\w+)$', produces.strip()).groups()
            if rsc in maps:
                raise Exception("Bad assumption. Resource produced by multiple reactions!")
            maps[rsc] = (int(count), consumes)
    return maps


def want(rsc_map, qty, rsc, have):
    needed_ore = 0
    if rsc == 'ORE':
        return qty
    get, requires = rsc_map[rsc]
    rsc_obtained = have.setdefault(rsc, 0)
    have[rsc] = 0
    while rsc_obtained < qty:
        for count, type_ in requires:
            needed_ore += want(rsc_map, count, type_, have)
        rsc_obtained += get
    have[rsc] += rsc_obtained - qty
    return needed_ore


def react(rsc_map, qty, rsc, have):
    if rsc == 'ORE':
        return False
    get, requires = rsc_map[rsc]
    success = True
    while have.setdefault(rsc, 0) < qty:
        allocated = {}
        for count, type_ in requires:
            if have.setdefault(type_, 0) < count:
                react(rsc_map, count, type_, have)
            if have[type_] < count:
                success = False
                break
            allocated[type_] = count
            have[type_] -= count
        if not success:
            # de-allocate required resources
            for type_, count in allocated.items():
                have[type_] += count
            return False
        # increase supply of our resource
        have[rsc] += get
    return True


def part1(path):
    data = read_file(path)
    # We want to produce 1 FUEL
    print(path, want(data, 1, 'FUEL', {}))


def part2_cycle_strategy(path):
    # we want to maximize the amount of fuel we can produce given 1000000000000 units of ORE
    available_ore = 1000000000000
    cycle_set = set()
    data = read_file(path)
    byproducts = {}
    ore_for1 = want(data, 1, 'FUEL', byproducts)
    # print(path, ore_for1, byproducts)
    fuel_per_batch = 1
    ore_per_batch = ore_for1
    cycle_set.add(tuple(byproducts.items()))
    while not all(v == 0 for v in byproducts.values()):
        ore_per_batch += want(data, 1, 'FUEL', byproducts)
        if ore_per_batch > available_ore:
            print(fuel_per_batch, "No good cycle")
            return
        fuel_per_batch += 1
        byproduct_tuple = tuple(byproducts.items())
        if byproduct_tuple in cycle_set:
            print("Found a cycle not at 0", byproducts)
            return
        cycle_set.add(byproduct_tuple)
    # print(fuel_per_batch, ore_per_batch)
    num_batches = available_ore // ore_per_batch
    fuel = num_batches * fuel_per_batch
    required_ore = num_batches * ore_per_batch
    while True:
        new_byproducts = dict(byproducts)
        needed = want(data, 1, 'FUEL', new_byproducts)
        if required_ore + needed > available_ore:
            break
        byproducts = new_byproducts
        required_ore += needed
        fuel += 1
    revert_to_ore(data, byproducts)
    required_ore -= byproducts.get('ORE', 0)
    byproducts['ORE'] = 0
    print(fuel, required_ore)


class StackSet(OrderedDict):
    def popitem(self, last=False):
        return super().popitem(last=last)[0]

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)

    def add(self, key):
        self[key] = key

    def update(self, iterable):
        for k in iterable:
            self.add(k)
        return self


def revert_to_ore(rsc_map, byproducts):
    to_process = StackSet().update(byproducts.keys())
    while to_process:
        rsc = to_process.popitem()
        if rsc == 'ORE':
            continue
        get, requires = rsc_map[rsc]
        if byproducts[rsc] > get:
            mult = byproducts[rsc] // get
            byproducts[rsc] -= get * mult
            for count, type_ in requires:
                byproducts[type_] += count * mult
                to_process.add(type_)


class FuelBatch(object):
    RSC_MAP = {}

    def __init__(self, ore, fuel, byproducts):
        self.ore = ore  # consumed
        self.fuel = fuel  # produced
        self.byproducts = defaultdict(lambda: 0, byproducts)  # left over

    def copy(self):
        return FuelBatch(self.ore, self.fuel, self.byproducts)

    def refund(self):
        revert_to_ore(self.RSC_MAP, self.byproducts)
        self.ore -= self.byproducts['ORE']
        self.byproducts['ORE'] = 0

    def react(self):
        while react(self.RSC_MAP, 1, 'FUEL', self.byproducts):
            self.fuel += self.byproducts['FUEL']
            self.byproducts['FUEL'] = 0
        # revert_to_ore(self.RSC_MAP, self.byproducts)
        # while react(self.RSC_MAP, 1, 'FUEL', self.byproducts):
        #     self.fuel += self.byproducts['FUEL']
        #     self.byproducts['FUEL'] = 0
        self.refund()
        # revert_to_ore(self.RSC_MAP, self.byproducts)

    def __mul__(self, qty):
        new_byproducts = {}
        for name, count in self.byproducts.items():
            new_byproducts[name] = count * qty
        ore = self.ore * qty
        fuel = self.fuel * qty
        result = FuelBatch(ore, fuel, new_byproducts)
        # result.react()
        result.refund()
        return result

    def __add__(self, other):
        new_byproducts = {}
        ore = self.ore + other.ore
        fuel = self.fuel + other.fuel
        for rsc in self.RSC_MAP.keys():
            new_byproducts[rsc] = self.byproducts.get(rsc, 0) + other.byproducts.get(rsc, 0)
        result = FuelBatch(ore, fuel, new_byproducts)
        # result.react()
        result.refund()
        return result


def batch_multiply(rsc_map, ore, fuel, byproducts, qty):
    new_byproducts = {}
    for name, count in byproducts.items():
        new_byproducts[name] = count * qty
    ore *= qty
    fuel *= qty
    while react(rsc_map, 1, 'FUEL', new_byproducts):
        fuel += new_byproducts['FUEL']
        new_byproducts['FUEL'] = 0
    revert_to_ore(rsc_map, new_byproducts)
    while react(rsc_map, 1, 'FUEL', new_byproducts):
        fuel += new_byproducts['FUEL']
        new_byproducts['FUEL'] = 0
    return ore, fuel, new_byproducts


def part2(path):
    # we want to maximize the amount of fuel we can produce given 1000000000000 units of ORE
    available_ore = 1000000000000
    data = read_file(path)
    FuelBatch.RSC_MAP = data
    byproducts = {}
    ore_for1 = want(data, 1, 'FUEL', byproducts)
    fuel_produced = 1
    batch1 = FuelBatch(ore_for1, fuel_produced, byproducts)
    print(path, batch1.fuel, batch1.ore)
    batch = batch1.copy()
    batches = [batch]
    while True:
        new_batch = batches[-1] * 2
        if new_batch.ore > available_ore:
            break
        batches.append(new_batch)
    # print(path, batches[-1].fuel, batches[-1].ore)
    idx = len(batches) - 1
    cur = batches[-1]
    while idx >= 0:
        if cur.ore + batches[idx].ore > available_ore:
            idx -= 1
            continue
        cur += batches[idx]
    cur.byproducts['ORE'] += available_ore - cur.ore
    cur.react()
    print(cur.fuel, cur.ore)


def main():
    #part1('example1.txt')
    #part1('example2.txt')
    #part1('example3.txt')
    #part1('example4.txt')
    #part1('example5.txt')
    part1('input.txt')
    part2('example3.txt')
    part2_cycle_strategy('example3.txt')
    part2('example4.txt')
    part2_cycle_strategy('example4.txt')
    part2('example5.txt')
    part2('input.txt')
    # part2_cycle_strategy('input.txt')


if __name__ == "__main__":
    main()
