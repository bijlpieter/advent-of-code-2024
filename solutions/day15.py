class Warehouse:
    def __init__(self, input: str) -> None:
        warehouse, moves = input.split("\n\n")
        self.moves = moves.replace("\n", "")
        rows = warehouse.split("\n")
        self.warehouse = [list(row) for row in rows]
        self.shape = len(rows), len(rows[0])
        self.robot = self.find_robot()

    def widen(self) -> None:
        widener = {"#": "##", "O": "[]", ".": "..", "@": "@."}
        self.warehouse = [
            list("".join(map(widener.__getitem__, row))) for row in self.warehouse
        ]
        self.robot = self.find_robot()

    def find_robot(self) -> tuple[int, int]:
        for i, row in enumerate(self.warehouse):
            for j, c in enumerate(row):
                if c == "@":
                    return (i, j)
        raise ValueError("No robot found")

    def can_push(self, r: int, c: int, dr: int, dc: int) -> bool:
        curr = self.warehouse[r][c]
        if curr == ".":
            return True
        if curr == "#":
            return False
        if curr == "O":
            return self.can_push(r + dr, c + dc, dr, dc)
        if curr in "[]":
            d = 1 if curr == "[" else -1
            one = self.can_push(r + dr, c + dc, dr, dc)
            two = self.can_push(r + dr, c + dc + d, dr, dc) if dr else True
            return one and two

        raise Exception(f"Invalid block: {curr}")

    def move(self, moving: str, r: int, c: int, dr: int, dc: int) -> None:
        curr = self.warehouse[r][c]
        if curr == ".":
            self.warehouse[r][c] = moving
        if curr == "O":
            self.move(curr, r + dr, c + dc, dr, dc)
            self.warehouse[r][c] = moving
        if curr in "[]":
            d, other = (1, "]") if curr == "[" else (-1, "[")
            self.move(curr, r + dr, c + dc, dr, dc)
            self.move(other, r + dr, c + dc + d, dr, dc) if dr else True
            self.warehouse[r][c] = moving
            if dr:
                self.warehouse[r][c + d] = "."

    def draw(self) -> None:
        print("\n".join("".join(row) for row in self.warehouse))

    def simulate(self) -> None:
        d = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
        r, c = self.robot
        for move in self.moves:
            # self.draw()
            # print(move)
            dr, dc = d[move]
            if self.can_push(r + dr, c + dc, dr, dc):
                self.move("@", r + dr, c + dc, dr, dc)
                self.warehouse[r][c] = "."
                r, c = r + dr, c + dc
        # self.draw()

    def gps_coordinates(self) -> list[int]:
        return [
            i * 100 + j
            for i, row in enumerate(self.warehouse)
            for j, c in enumerate(row)
            if c in "[O"
        ]


def parser(input: str) -> Warehouse:
    return Warehouse(input)


def part1(warehouse: Warehouse) -> int:
    warehouse.simulate()
    return sum(warehouse.gps_coordinates())


def part2(warehouse: Warehouse) -> int:
    warehouse.widen()
    warehouse.simulate()
    return sum(warehouse.gps_coordinates())
