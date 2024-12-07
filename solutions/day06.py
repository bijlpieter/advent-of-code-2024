class Lab:
    def __init__(self, input: str) -> None:
        rows = input.split("\n")
        self.lab = [[c == "#" for c in row] for row in rows]
        self.find_guard(rows)

    def find_guard(self, rows: list[str]) -> None:
        d = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
        for i, row in enumerate(rows):
            for j, c in enumerate(row):
                if c in d:
                    self.guard = (i, j)
                    self.direction = d[c]
                    return
        raise ValueError("No guard found")

    def shape(self) -> tuple[int, int]:
        return len(self.lab), len(self.lab[0])

    def simulate(
        self, obstacle: tuple[int, int] | None = None
    ) -> tuple[bool, set[tuple[int, int, int, int]]]:
        h, w = self.shape()
        r, c = self.guard
        dr, dc = self.direction
        visited = {(r, c, dr, dc)}
        next_dir = {(0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1)}

        while 0 <= r + dr < h and 0 <= c + dc < w:
            while self.lab[r + dr][c + dc] or (r + dr, c + dc) == obstacle:
                dr, dc = next_dir[dr, dc]

            r, c = r + dr, c + dc
            item = (r, c, dr, dc)
            if item in visited:
                return True, visited
            else:
                visited.add(item)

        return False, visited


def parser(input: str) -> Lab:
    return Lab(input)


def part1(lab: Lab) -> int:
    loop, path = lab.simulate()
    return len({step[:2] for step in path})


def part2(lab: Lab) -> int:
    before = {
        step[:2] for step in lab.simulate()[1] if lab.simulate(obstacle=step[:2])[0]
    }
    return len(before)
