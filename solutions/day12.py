from collections.abc import Generator
from typing import Literal


class Garden:
    def __init__(self, input: str) -> None:
        self.grid = input.split("\n")

        h, w = len(self.grid), len(self.grid[0])
        self.shape = h, w
        self.labels = [[-1] * w for _ in range(h)]
        self.regions = 0
        self.regionify()

    def label_at(self, r: int, c: int) -> int:
        h, w = self.shape
        return self.labels[r][c] if 0 <= r < h and 0 <= c < w else -1

    def neighbors(self, r: int, c: int) -> Generator[tuple[int, int]]:
        h, w = self.shape
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if 0 <= r + dr < h and 0 <= c + dc < w:
                yield r + dr, c + dc

    def corners(self, r: int, c: int) -> Generator[tuple[bool, bool, bool]]:
        h, w = self.shape
        for (r1, c1), (r2, c2), (r3, c3) in [
            ((0, 1), (1, 0), (1, 1)),
            ((0, 1), (-1, 0), (-1, 1)),
            ((0, -1), (1, 0), (1, -1)),
            ((0, -1), (-1, 0), (-1, -1)),
        ]:
            label = self.label_at(r, c)
            yield (
                label == self.label_at(r + r1, c + c1),
                label == self.label_at(r + r2, c + c2),
                label == self.label_at(r + r3, c + c3),
            )

    def floodfill(self, row: int, col: int, label: int) -> None:
        if self.label_at(row, col) != -1:
            return

        plant = self.grid[row][col]
        self.labels[row][col] = label
        for r, c in self.neighbors(row, col):
            if self.grid[r][c] == plant:
                self.floodfill(r, c, label)

    def regionify(self) -> None:
        h, w = self.shape
        for r in range(h):
            for c in range(w):
                if self.labels[r][c] == -1:
                    self.floodfill(r, c, self.regions)
                    self.regions += 1

    def num_fences(self, row: int, col: int) -> int:
        neighbors = list(self.neighbors(row, col))
        return (
            sum(self.label_at(row, col) != self.label_at(r, c) for r, c in neighbors)
            + 4
            - len(neighbors)
        )

    def perimeter(self, region: int) -> int:
        h, w = self.shape
        return sum(
            self.num_fences(r, c)
            for r in range(h)
            for c in range(w)
            if self.label_at(r, c) == region
        )

    def num_corners(self, r0: int, c0: int) -> int:
        corners = list(self.corners(r0, c0))
        out = sum(l1 == l2 and not (l2 and l3) for l1, l2, l3 in corners)
        # print(corners, "->", out)
        return out

    def num_sides(self, region: int) -> int:
        h, w = self.shape
        return sum(
            self.num_corners(r, c)
            for r in range(h)
            for c in range(w)
            if self.label_at(r, c) == region
        )

    def area(self, region: int) -> int:
        return sum(label == region for row in self.labels for label in row)

    def total_fencing_price(self, how: Literal["perimeter", "sides"]) -> int:
        sides = self.perimeter if how == "perimeter" else self.num_sides
        return sum(sides(region) * self.area(region) for region in range(self.regions))


def parser(input: str) -> Garden:
    return Garden(input)


def part1(garden: Garden) -> int:
    return garden.total_fencing_price(how="perimeter")


def part2(garden: Garden) -> int:
    return garden.total_fencing_price(how="sides")
