import re

pattern = r"""
Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)
""".strip()


def parser(input: str) -> list[tuple[int, ...]]:
    return [tuple(map(int, match)) for match in re.findall(pattern, input)]


def solve(a: int, b: int, c: int, d: int, e: int, f: int) -> tuple[float, float]:
    det = a * d - c * b
    return (e * d - c * f) / det, (a * f - b * e) / det


def play(games: list[tuple[int, ...]], offset: int = 0) -> int:
    out = sum(
        x * 3 + y
        for a, b, c, d, e, f in games
        for x, y in [solve(a, b, c, d, e + offset, f + offset)]
        if x.is_integer() and y.is_integer()
    )
    return int(out)


def part1(games: list[tuple[int, ...]]) -> int:
    return play(games)


def part2(games: list[tuple[int, ...]]) -> int:
    return play(games, offset=10000000000000)
