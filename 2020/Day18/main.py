

examples = [
    "1 + 2 * 3 + 4 * 5 + 6",
    "1 + (2 * 3) + (4 * (5 + 6))",
    "2 * 3 + (4 * 5)",
    "5 + (8 * 3 + 9 + 3 * 4 * 3)",
    "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
    "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
]


OPS = {
    '*': lambda x, y: x * y,
    '+': lambda x, y: x + y
}


def read_file(path):
    with open(path, "r") as f:
        return list(line.strip() for line in f)


def append_value(stack, val):
    if stack[-1] in OPS:
        op = stack.pop()
        other = stack.pop()
        val = OPS[op](other, val)
    stack.append(val)


def solve_expression(exp):
    stack = [None]
    for c in exp:
        if c == ' ':
            continue
        elif c in '0123456789':
            append_value(stack, int(c))
        elif c == '(':
            stack.append('(')
        elif c == ')':
            val = stack.pop()
            if stack.pop() != '(':  # This *should* be the open paren
                raise Exception("Unmatched close paren!")
            append_value(stack, val)
        elif c in OPS:
            stack.append(c)
        else:
            raise Exception("bad input")
    answer = stack.pop()
    # print("{} = {}".format(answer, exp))
    return answer


def examples1():
    for exp in examples:
        solve_expression(exp)


def part1(path):
    data = read_file(path)
    print("Total:", sum(solve_expression(exp) for exp in data))


def append_value2(stack, val):
    if stack[-1] == '+':
        op = stack.pop()
        other = stack.pop()
        val = OPS[op](other, val)
    stack.append(val)


def finalize_expression(stack):
    val = stack.pop()
    while stack[-1] != '(':
        op = stack.pop()
        other = stack.pop()
        val = OPS[op](other, val)
    if stack.pop() != '(':  # This *should* be the open paren
        raise Exception("Unmatched close paren!")
    append_value2(stack, val)


def solve_expression2(exp):
    stack = [None, '(']
    for c in exp:
        if c == ' ':
            continue
        elif c in '0123456789':
            append_value2(stack, int(c))
        elif c == '(':
            stack.append('(')
        elif c == ')':
            finalize_expression(stack)
        elif c in OPS:
            stack.append(c)
        else:
            raise Exception("bad input")
    finalize_expression(stack)
    answer = stack.pop()
    # print("{} = {}".format(answer, exp))
    return answer


def examples2():
    for exp in examples:
        solve_expression2(exp)


def part2(path):
    data = read_file(path)
    print("Total:", sum(solve_expression2(exp) for exp in data))


def main():
    # examples1()
    part1("input.txt")
    # examples2()
    part2("input.txt")


if __name__ == "__main__":
    main()
