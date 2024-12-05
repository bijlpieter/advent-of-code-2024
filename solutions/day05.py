from functools import cmp_to_key


def middle(update: list[int]) -> int:
    return update[len(update) // 2]


def parser(input: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules, updates = input.split("\n\n")
    return [
        (int(left), int(right))
        for rule in rules.split("\n")
        for left, right in [rule.split("|")]
    ], [list(map(int, update.split(","))) for update in updates.split("\n")]


def is_legal(update: list[int], rules: list[tuple[int, int]]) -> bool:
    return all(
        before not in update
        or after not in update
        or update.index(before) < update.index(after)
        for before, after in rules
    )


def part1(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    return sum(middle(update) for update in updates if is_legal(update, rules))


def key(groups: dict[int, list[int]]):
    return cmp_to_key(lambda le, ri: -1 if le in groups and ri in groups[le] else 1)


def part2(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    lefts = {rule[0] for rule in rules}
    groups = {left: [ri for le, ri in rules if le == left] for left in set(lefts)}
    return sum(
        middle(sorted(update, key=key(groups)))
        for update in updates
        if not is_legal(update, rules)
    )
