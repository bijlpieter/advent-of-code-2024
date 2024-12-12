from collections import defaultdict
from collections.abc import Callable, Generator
from fractions import Fraction
from itertools import combinations


class Roof:
    def __init__(self, input: str) -> None:
        rows = input.split("\n")
        self.shape = len(rows), len(rows[0])

        self.antennas = defaultdict(list)
        for i, row in enumerate(rows):
            for j, char in enumerate(row):
                self.antennas[char].append((i, j))
        del self.antennas["."]

    def antinodes(
        self, one: tuple[int, int], two: tuple[int, int]
    ) -> list[tuple[int, int]]:
        h, w = self.shape
        r1, c1 = one
        r2, c2 = two
        dr, dc = r2 - r1, c2 - c1

        nodes = [(r1 - dr, c1 - dc), (r2 + dr, c2 + dc)]
        return [(r, c) for r, c in nodes if 0 <= r < h and 0 <= c < w]

    def yield_line(
        self, start: tuple[int, int], delta: tuple[int, int]
    ) -> Generator[tuple[int, int]]:
        h, w = self.shape
        r, c = start
        dr, dc = delta

        while 0 <= r < h and 0 <= c < w:
            yield r, c
            r, c = r + dr, c + dc

        r, c = start
        while 0 <= r < h and 0 <= c < w:
            yield r, c
            r, c = r - dr, c - dc

    def resonance(
        self, one: tuple[int, int], two: tuple[int, int]
    ) -> list[tuple[int, int]]:
        r1, c1 = one
        r2, c2 = two
        dr, dc = Fraction(r2 - r1, c2 - c1).as_integer_ratio()
        return list(self.yield_line((r1, c1), (dr, dc)))

    def solver(
        self,
        antinodes: Callable[[tuple[int, int], tuple[int, int]], list[tuple[int, int]]],
    ) -> int:
        return len(
            {
                antinode
                for freq, locations in self.antennas.items()
                for one, two in combinations(locations, 2)
                for antinode in antinodes(one, two)
            }
        )


def parser(input: str) -> Roof:
    return Roof(input)


def part1(roof: Roof) -> int:
    return roof.solver(roof.antinodes)


def part2(roof: Roof) -> int:
    return roof.solver(roof.resonance)
