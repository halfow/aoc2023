from pathlib import Path
from typing import Sequence
from rich import print
from itertools import chain

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text().split("\n\n")
example = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""".strip().split("\n\n")


def reflection(grid: Sequence[Sequence[str]], center: int) -> int:
    """Calculate the reflection error with the given center."""
    upper, lower = grid[:center], grid[center:]
    compare_rows = zip(reversed(upper), lower, strict=False)
    compare_chars = chain.from_iterable(zip(x, y) for x, y in compare_rows)
    return sum(a != b for a, b in compare_chars)


def _finder(grid: Sequence[Sequence[str]], error: int):
    """Get the first index that matches the given reflection error."""
    it = (n for n in range(1, len(grid)) if reflection(grid, n) == error)
    return next(it, 0)


def mirrors(text: str, error: int):
    """Summarize the score."""
    horizontal = text.splitlines()
    vertical = tuple(zip(*horizontal))
    return 100 * _finder(horizontal, error) + _finder(vertical, error)


part_1 = sum(mirrors(x, error=0) for x in validation)
part_2 = sum(mirrors(x, error=1) for x in validation)
print(f"{part_1=}", f"{part_2=}", sep="\n")
