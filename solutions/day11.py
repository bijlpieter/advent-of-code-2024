from functools import cache


def parser(input: str) -> list[int]:
    return list(map(int, input.split(" ")))


def blink(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    digits = str(stone)
    if len(digits) % 2 == 0:
        half = len(digits) // 2
        return [int(digits[:half]), int(digits[half:])]

    return [stone * 2024]


@cache
def simulate(stone: int, blinks: int) -> int:
    return 1 if blinks == 0 else sum(simulate(new, blinks - 1) for new in blink(stone))


def evolve(stones: list[int], blinks: int) -> int:
    return sum(simulate(stone, blinks) for stone in stones)


def part1(stones: list[int]) -> int:
    return evolve(stones, 25)


def part2(stones: list[int]) -> int:
    return evolve(stones, 75)
