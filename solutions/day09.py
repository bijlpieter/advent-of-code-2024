from collections.abc import Generator, Iterable
from itertools import zip_longest


def disk(diskmap: str) -> list[int]:
    return [
        id // 2 if id % 2 == 0 else -1
        for id, c in enumerate(diskmap)
        for _ in range(int(c))
    ]


def compress(files: list[int]) -> Generator[int]:
    le, ri = 0, len(files) - 1
    while le <= ri:
        while files[ri] == -1:
            ri -= 1

        yield files[le] if files[le] != -1 else files[ri]
        ri -= files[le] == -1
        le += 1


def checksum(compressed: Iterable[int]) -> int:
    return sum(i * id for i, id in enumerate(compressed) if id != -1)


def part1(input: str) -> int:
    return checksum(compress(disk(input)))


def filemanager(diskmap: str):
    return [
        (id, int(file), int(free))
        for id, (file, free) in enumerate(
            zip_longest(diskmap[::2], diskmap[1::2], fillvalue="0")
        )
    ]


def insert_after(curr: int, fs: list[tuple[int, int, int]], space: int) -> int:
    for idx, (id, size, free) in enumerate(fs):
        if id == curr:
            return -1
        if free >= space:
            return idx
    return -1


def defragment(fs: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    for id1, size1, free1 in fs[::-1]:
        idx = insert_after(id1, fs, size1)
        if idx == -1:
            continue

        id2, size2, free2 = fs[idx]
        fs[idx : idx + 1] = [(id2, size2, 0), (id1, size1, free2 - size1)]

        for i in reversed(range(len(fs))):
            if fs[i][0] == id1:
                fs[i - 1 : i + 1] = [
                    (*fs[i - 1][:2], fs[i - 1][2] + fs[i][1] + fs[i][2])
                ]
                break

    return fs


def display(fs: list[tuple[int, int, int]]) -> list[int]:
    return [out for id, size, free in fs for out in [id] * size + [-1] * free]


def part2(input: str) -> int:
    return checksum(display(defragment(filemanager(input))))
