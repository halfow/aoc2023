from pathlib import Path
from itertools import pairwise
from typing import Iterator, Sequence

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".strip()


def parse(text: str) -> Iterator[tuple[int, ...]]:
    for line in text.splitlines():
        yield tuple(map(int, line.split()))


def diff(sequence: Sequence[int]) -> Iterator[int]:
    new = tuple(a - b for a, b in pairwise(sequence))
    if any(new):
        yield from diff(new)
    yield sequence[0]


def part1(text: str) -> int:
    return sum(sum(diff(series[::-1])) for series in parse(text))


def part2(text: str) -> int:
    return sum(sum(diff(series)) for series in parse(text))


print(f"{part1(example)=}")
print(f"{part1(validation)=}")

print(f"{part2(example)=}")
print(f"{part2(validation)=}")
