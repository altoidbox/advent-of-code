import argparse


def load(path):
    data = []
    with open(path) as f:
        for line in f:
            data.append([int(x) for x in line.split()])
    return data


def is_safe(report):
    direction = 0
    for i in range(1, len(report)):
        diff = report[i] - report[i-1]
        if not (-3 <= diff <= 3) or diff == 0:
            # print('too big or 0', diff)
            break
        if direction < 0 and diff > 0:
            # print('lt')
            break
        if direction > 0 and diff < 0:
            # print('gt')
            break
        direction = diff
    else:
        # print(f'good: {report}')
        return True, -1
    # print(f'bad: {report}')
    return False, i - 1


def part1(path):
    count = 0
    data = load(path)
    for report in data:
        result, _ = is_safe(report)
        if result:
            count += 1
        
    print(count)


def part2(path):
    count = 0
    data = load(path)
    for i, report in enumerate(data):
        result, idx = is_safe(report)
        offs = 0
        if not result:
            for offs in (-1, 0, 1):
                if not (0 <= idx + offs < len(report)):
                    continue
                copy = list(report)
                copy.pop(idx+offs)
                result, _ = is_safe(copy)
                if result:
                    break

        if result:
            # print(f'{i}: rem {idx + offs} {report}')
            count += 1        
    print(count)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    part1(args.path)
    part2(args.path)


main()
