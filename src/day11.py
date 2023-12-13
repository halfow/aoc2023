from pathlib import Path
from typing import Iterator, Tuple, Sequence
from bisect import bisect_left
from itertools import combinations


file_name: str = Path(__file__).with_suffix(".txt").name
dir_name: Path = Path(__file__).parent.with_name("input")
validation: str = (dir_name / file_name).read_text()
example: str = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".strip()


def parse(text: str) -> Iterator[Tuple[int, int]]:
    yield from (
        (x, y)
        for y, line in enumerate(text.splitlines())
        for x, character in enumerate(line)
        if character == "#"
    )


def space(data: Sequence[Tuple[int, int]], size: int) -> int:
    row, col = zip(*data)
    x_void = sorted(set(range(min(row), max(row))).difference(row))
    y_void = sorted(set(range(min(col), max(col))).difference(col))
    expanded = (
        (x + bisect_left(x_void, x) * size, y + bisect_left(y_void, y) * size)
        for x, y in data
    )
    return sum(abs(c - a) + abs(d - b) for (a, b), (c, d) in combinations(expanded, 2))


example_data = tuple(parse(example))
validation_data = tuple(parse(validation))

print(f"Part1 example   :{space(example_data, 1):>14}")
print(f"Part1 validation:{space(validation_data, 1):>14}")

print(f"Part2 example   :{space(example_data, 999999):>14}")
print(f"Part2 validation:{space(validation_data, 999999):>14}")
