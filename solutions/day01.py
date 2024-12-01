from collections import Counter


def parser(input: str) -> tuple[list[int], list[int]]:
    rows = input.split("\n")
    pairs = [tuple(map(int, row.split("   "))) for row in rows]
    return tuple(zip(*pairs))


def part1(input: str) -> int:
    col1, col2 = parser(input)
    return sum(abs(left - right) for left, right in zip(sorted(col1), sorted(col2)))


def part2(input: str) -> int:
    col1, col2 = parser(input)
    counter = Counter(col2)
    return sum(val * counter.get(val, 0) for val in col1)
