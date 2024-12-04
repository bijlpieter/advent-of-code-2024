from collections.abc import Generator, Sequence


def parser(input: str) -> list[list[str]]:
    return [input.split("\n")]


def shape(grid: Sequence[Sequence]) -> tuple[int, int]:
    return len(grid), len(grid[0])


def sliding_window_view(grid: list[str], mask: list[list[bool]]) -> Generator[str]:
    rows, cols = shape(grid)
    mrows, mcols = shape(mask)
    for y in range(rows - mrows + 1):
        for x in range(cols - mcols + 1):
            masked = "".join(
                grid[y + i][x + j]
                for i in range(mrows)
                for j in range(mcols)
                if mask[i][j]
            )
            yield masked
            yield masked[::-1]


def part1(grid: list[str]) -> int:
    diags = [
        [True, False, False, False],
        [False, True, False, False],
        [False, False, True, False],
        [False, False, False, True],
    ]

    masks = [
        [[True, True, True, True]],
        [[True], [True], [True], [True]],
        diags,
        diags[::-1],
    ]

    return sum(
        view == "XMAS" for mask in masks for view in sliding_window_view(grid, mask)
    )


def part2(grid: list[str]) -> int:
    mask = [[True, False, True], [False, True, False], [True, False, True]]
    return sum(view in {"MMASS", "MSAMS"} for view in sliding_window_view(grid, mask))
