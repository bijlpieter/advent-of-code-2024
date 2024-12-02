import importlib
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "day, part1, part2",
    [
        (1, 2367773, 21271939),
        (2, 287, 354),
        (3, NotImplemented, NotImplemented),
        (4, NotImplemented, NotImplemented),
        (5, NotImplemented, NotImplemented),
        (6, NotImplemented, NotImplemented),
        (7, NotImplemented, NotImplemented),
        (8, NotImplemented, NotImplemented),
        (9, NotImplemented, NotImplemented),
        (10, NotImplemented, NotImplemented),
        (12, NotImplemented, NotImplemented),
        (13, NotImplemented, NotImplemented),
        (14, NotImplemented, NotImplemented),
        (15, NotImplemented, NotImplemented),
        (16, NotImplemented, NotImplemented),
        (17, NotImplemented, NotImplemented),
        (18, NotImplemented, NotImplemented),
        (19, NotImplemented, NotImplemented),
        (20, NotImplemented, NotImplemented),
        (21, NotImplemented, NotImplemented),
        (22, NotImplemented, NotImplemented),
        (23, NotImplemented, NotImplemented),
        (24, NotImplemented, NotImplemented),
        (25, NotImplemented, NotImplemented),
    ],
)
def test_solutions(day, part1, part2):
    sol = importlib.import_module(f"solutions.day{day:0>2}")
    path = Path.cwd().joinpath("data", f"day{day:0>2}.txt")
    txt = path.read_text().strip() if path.exists() else ""
    assert sol.part1(txt) == part1
    assert sol.part2(txt) == part2
