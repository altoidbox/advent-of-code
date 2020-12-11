import sys

FILE = "input.txt"
#FILE = "example1.txt"
#FILE = "example2.txt"


def read_file(path):
    with open(path, "r") as f:
        data = [int(d) for d in f.read().strip()]
    return data


def parse_image(data, width, height):
    layers = []
    while len(layers) * width * height < len(data):
        start = len(layers) * width * height
        rows = []
        for h in range(height):
            rows.append(data[start + width*h:start + width*h + width])
        layers.append(rows)
    return layers


def count_value(layer, value):
    total = 0
    for row in layer:
        total += len(list(filter(lambda d: d == value, row)))
    return total


def part1():
    # print(parse_image(read_file("example1.txt"), 3, 2))
    image = parse_image(read_file("input.txt"), 25, 6)
    vals = []
    for i, layer in enumerate(image):
        vals.append((count_value(layer, 0), i))
    _, layeridx = min(vals)
    print(count_value(image[layeridx], 1) * count_value(image[layeridx], 2))


def part2():
    image = parse_image(read_file("input.txt"), 25, 6)
    base = image[0]
    for layer in image[1:]:
        for row, row_vals in enumerate(layer):
            for col, val in enumerate(row_vals):
                if base[row][col] == 2:
                    base[row][col] = val
    for row in base:
        print("".join('@' if v else ' ' for v in row))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
