import re

FILE = "input.txt"
# FILE = "example1.txt"


def read_file(path):
    with open(path, "r") as f:
        foods = []
        for line in f:
            ingredients, contains = re.match(r'^(.*) \(contains (.*)\)', line).groups()
            ingredients = set(ingredients.split(' '))
            contains = contains.split(', ')
            foods.append((ingredients, contains))

        return foods


def part1():
    foods = read_file(FILE)
    possibles = {}
    all_ingredients = set()
    for ingredients, allergens in foods:
        all_ingredients.update(ingredients)
        for allergen in allergens:
            if allergen not in possibles:
                possibles[allergen] = set(ingredients)
            else:
                possibles[allergen].intersection_update(ingredients)
    # print(possibles)
    certainties = {}
    new_certainties = list(filter(lambda item: len(item[1]) == 1, possibles.items()))
    while len(new_certainties):
        for allergen, ingredients in new_certainties:
            possibles.pop(allergen)

        for allergen, ingredients in new_certainties:
            ingredient = ingredients.pop()
            all_ingredients.discard(ingredient)
            certainties[allergen] = ingredient
            for other_ingredients in possibles.values():
                other_ingredients.discard(ingredient)
        new_certainties = list(filter(lambda item: len(item[1]) == 1, possibles.items()))
    print(certainties)
    # print(possibles)
    # print(all_ingredients)
    answer = 0
    for ingredients, allergens in foods:
        answer += len(all_ingredients.intersection(ingredients))
    print(answer)
    return certainties


def part2(allergen_map):
    print(",".join(map(lambda item: item[1], sorted(allergen_map.items()))))


def main():
    allergen_map = part1()
    part2(allergen_map)


if __name__ == "__main__":
    main()
