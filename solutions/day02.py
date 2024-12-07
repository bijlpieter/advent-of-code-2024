from itertools import pairwise


def parser(input: str) -> list[list[int]]:
    return [list(map(int, row.split(" "))) for row in input.split("\n")]


def is_safe(report: list[int]) -> bool:
    diff = [a - b for a, b in pairwise(report)]

    monotonic = all(d < 0 for d in diff) or all(d > 0 for d in diff)
    gradual = all(1 <= abs(d) <= 3 for d in diff)

    return monotonic and gradual


def problem_dampener(report: list[int]) -> list[list[int]]:
    return [
        [val for i, val in enumerate(report) if i != idx] for idx in range(len(report))
    ]


def part1(reports: list[list[int]]) -> int:
    return sum(map(is_safe, reports))


def part2(reports: list[list[int]]) -> int:
    return sum(
        any(is_safe(dampened) for dampened in problem_dampener(report))
        for report in reports
    )
