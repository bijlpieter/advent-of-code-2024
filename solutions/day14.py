import os
import re

pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
W, H = 101, 103


def parser(input: str) -> list[tuple[int, ...]]:
    return [tuple(map(int, match)) for match in re.findall(pattern, input)]


def step(x, y, dx, dy) -> tuple[int, int, int, int]:
    return (x + dx) % W, (y + dy) % H, dx, dy


def simulate(
    robots: list[tuple[int, int, int, int]],
) -> list[tuple[int, int, int, int]]:
    return [step(x, y, dx, dy) for x, y, dx, dy in robots]


def sign(val: int) -> int:
    return (val > 0) - (val < 0)


def quadrant(x: int, y: int) -> tuple[int, int]:
    return sign(W // 2 - x), sign(H // 2 - y)


def count(robots: list[tuple[int, int, int, int]], q: tuple[int, int]) -> int:
    return sum(quadrant(x, y) == q for x, y, dx, dy in robots)


def safety_score(robots: list[tuple[int, int, int, int]]) -> int:
    return (
        count(robots, q=(-1, -1))
        * count(robots, q=(1, -1))
        * count(robots, q=(-1, 1))
        * count(robots, q=(1, 1))
    )


def part1(robots: list[tuple[int, int, int, int]]) -> int:
    for _ in range(100):
        robots = simulate(robots)
    return safety_score(robots)


def draw(robots: list[tuple[int, int, int, int]], i) -> None:
    os.system("cls")
    grid = [[False] * W for _ in range(H)]
    for x, y, dx, dy in robots:
        grid[y][x] = True
    for row in grid:
        print("".join(" #"[b] for b in row))
    input(i)


def part2(robots: list[tuple[int, int, int, int]]) -> int:
    # for i in range(100000000000):
    #     if (i % H == 19 or i % W == 74) and i > 8000:
    #         draw(robots, i)
    #     robots = simulate(robots)
    return 8053
