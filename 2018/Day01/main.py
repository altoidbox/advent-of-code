import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


def part1(args):
    value = 0
    with open(args.input, 'rb') as f:
        for line in f:
            line_value = int(line.strip())
            new_value = value + line_value
            print("{}: {} += {} == {}".format(line, value, line_value, new_value))
            value = new_value

    print("\nFinal Result: {}".format(value))


def part2(args):
    value = 0
    seen_frequencies = set()
    while True:
        with open(args.input, 'rb') as f:
            for line in f:
                line_value = int(line.strip())
                new_value = value + line_value
                print("{}: {} += {} == {}".format(line, value, line_value, new_value))
                value = new_value
                if value not in seen_frequencies:
                    seen_frequencies.add(value)
                else:

                    print("\nFinal Result: {}".format(value))
                    return


if not args.part2:
    part1(args)
else:
    part2(args)

