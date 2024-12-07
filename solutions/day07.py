import multiprocessing
from collections.abc import Callable, Sequence
from itertools import compress, product, repeat
from operator import add, mul


def parse_line(line: str) -> tuple[int, list[int]]:
    total, values = line.split(": ")
    return int(total), [int(val) for val in values.split(" ")]


def parser(input: str) -> list[tuple[int, list[int]]]:
    return [parse_line(line) for line in input.split("\n")]


def compute(values: list[int], operators: Sequence[Callable[[int, int], int]]) -> int:
    acc, *values = values
    for val, op in zip(values, operators):
        acc = op(acc, val)
    return acc


def is_solvable(
    total: int, values: list[int], operators: Sequence[Callable[[int, int], int]]
) -> bool:
    return any(
        compute(values, ops) == total for ops in product(operators, repeat=len(values))
    )


def part1(equations: list[tuple[int, list[int]]]) -> int:
    return sum(
        total for total, values in equations if is_solvable(total, values, [add, mul])
    )


def concat(left: int, right: int) -> int:
    return int(f"{left}{right}")


def part2(equations: list[tuple[int, list[int]]]) -> int:
    totals, values = zip(*equations)
    with multiprocessing.Pool() as pool:
        results = pool.starmap(
            is_solvable, zip(totals, values, repeat([add, mul, concat]))
        )
    return sum(compress(totals, results))
