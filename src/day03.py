from pathlib import Path
import re
from operator import mul

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text().strip()
example = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip()


def to_kernel(i, row_length):
    """3x3 kernel"""
    yield i - 1
    yield i + 1
    yield from (i - row_length + k for k in (-1, 0, 1))
    yield from (i + row_length + k for k in (-1, 0, 1))


def party(text, pattern):
    numbers = tuple((int(m[0]), range(*m.span())) for m in re.finditer(r"\d+", text))
    line = text.find("\n") + 1
    gears = (set(to_kernel(m.start(), line)) for m in re.finditer(pattern, text))
    for gear in gears:
        yield [ratio for ratio, span in numbers if not gear.isdisjoint(span)]


def part1(text):
    return sum(map(sum, party(text, r"[^0-9.\s]")))


def part2(text):
    return sum(mul(*x) for x in party(text, r"\*") if len(x) == 2)  # noqa: PLR2004


print(f"{part1(example)=}")
print(f"{part1(validation)=}")

print(f"{part2(example)=}")
print(f"{part2(validation)=}")
