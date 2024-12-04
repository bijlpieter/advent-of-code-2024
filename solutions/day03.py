import re


def part1(input: str) -> int:
    return sum(
        int(left) * int(right)
        for left, right in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", input)
    )


def part2(input: str) -> int:
    take = True
    values = []
    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", input)

    for left, right, do, dont in matches:
        if do == "do()":
            take = True
        elif dont == "don't()":
            take = False
        elif take:
            values.append(int(left) * int(right))

    return sum(values)
