import importlib
import sys
import time
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from datetime import datetime, timedelta
from functools import partial
from inspect import signature
from pathlib import Path
from types import NotImplementedType

import requests


def download(day: int) -> str:
    if datetime.now() < datetime(year=2024, month=12, day=day, hour=6):
        return ""

    cookie = {"session": Path("cookie.txt").read_text().strip()}
    res = requests.get(f"https://adventofcode.com/2024/day/{day}/input", cookies=cookie)

    path = Path.cwd() / "data" / f"day{day:0>2}.txt"
    path.write_text(res.text)
    return res.text


def get_input(day: int) -> str:
    path = Path.cwd() / "data" / f"day{day:0>2}.txt"
    txt = path.read_text() if path.exists() else download(day)
    return txt.strip()


def run_part(
    part: Callable[[str], int | NotImplementedType], input
) -> tuple[str, timedelta]:
    sig = signature(part)
    if len(sig.parameters) == 1:
        input = [input]

    start = time.perf_counter()
    try:
        out = part(*input)
        end = time.perf_counter()
        return str(out), timedelta(seconds=end - start)
    except Exception as exc:
        end = time.perf_counter()
        return exc.__class__.__name__, timedelta(seconds=end - start)


def run_parts(
    day: int,
) -> tuple[
    Callable[[], tuple[str, timedelta]],
    Callable[[], tuple[str, timedelta]],
]:
    txt = get_input(day)
    sol = importlib.import_module(f"solutions.day{day:0>2}")
    i1 = sol.parser(txt) if hasattr(sol, "parser") else txt
    i2 = deepcopy(i1)
    return partial(run_part, sol.part1, i1), partial(run_part, sol.part2, i2)


def run_day(day: int):
    part1, part2 = run_parts(day)

    p1, t1 = part1()
    print(f"Part 1: {format_result(p1, t1)}")

    p2, t2 = part2()
    print(f"Part 2: {format_result(p2, t2)}")


def format_result(result: str | None = None, td: timedelta = timedelta()) -> str:
    if result is None:
        return "... Running ...".ljust(40)
    if result == "NotImplemented":
        return result.ljust(40)

    timed = f"({td})"
    return result + " " * (40 - len(timed + result)) + timed


def run_days(days: list[int] | None = None) -> None:
    days = list(range(1, 26)) if days is None else [int(day) for day in days]

    print(f"Day: | {'Part 1:': <40} | {'Part 2:': <40}")
    print("=" * 90)
    for day in days:
        print(f"{day: >4} | {format_result()} | {format_result()}")

    lines = dict(zip(days, range(len(days), 0, -1)))

    results = {}

    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(f): (day, part)
            for day in days
            for part, f in enumerate(run_parts(int(day)))
        }

        for future in as_completed(futures):
            day, part = futures[future]
            results[day, part] = future.result()

            count = lines[day]
            p1 = results.get((day, 0), (None, timedelta()))
            p2 = results.get((day, 1), (None, timedelta()))

            print(f"\033[{count}F", end="")

            print(f"{day: >4} | {format_result(*p1)} | {format_result(*p2)}")
            print(f"\033[{count}E", end="")


def main():
    if len(sys.argv) == 1 or sys.argv[1] == "all":
        run_days()
    elif len(sys.argv) <= 2:
        run_day(int(sys.argv[1]))
    else:
        run_days([int(d) for d in sys.argv[1:]])


if __name__ == "__main__":
    main()
