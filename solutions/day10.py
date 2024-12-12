from collections.abc import Callable, Generator


class Map:
    def __init__(self, input: str) -> None:
        self.grid = [[int(c) for c in row] for row in input.split("\n")]
        self.shape = len(self.grid), len(self.grid[0])

    def trailheads(self) -> Generator[tuple[int, int]]:
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c == 0:
                    yield i, j

    def value_at(self, pos: tuple[int, int]) -> int:
        r, c = pos
        return self.grid[r][c]

    def neighbors(self, pos: tuple[int, int]) -> Generator[tuple[int, int]]:
        h, w = self.shape
        r, c = pos
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if 0 <= r + dr < h and 0 <= c + dc < w:
                yield r + dr, c + dc

    def dfs_walk_trail[T](
        self,
        pos: tuple[int, int],
        base_case: Callable[[tuple[int, int]], T],
        reducer: Callable[[list[T]], T],
    ) -> T:
        return (
            base_case(pos)
            if self.value_at(pos) == 9
            else reducer(
                [
                    self.dfs_walk_trail(neighbor, base_case, reducer)
                    for neighbor in self.neighbors(pos)
                    if self.value_at(neighbor) == self.value_at(pos) + 1
                ]
            )
        )


def parser(input: str) -> Map:
    return Map(input)


def part1(map: Map) -> int:
    return sum(
        len(map.dfs_walk_trail(pos, lambda x: {x}, lambda x: set().union(*x)))
        for pos in map.trailheads()
    )


def part2(map: Map) -> int:
    return sum(
        map.dfs_walk_trail(pos, lambda _: 1, lambda x: sum(x))
        for pos in map.trailheads()
    )
