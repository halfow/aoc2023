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


def part1(text):
    # NOTE: Part numbers are never adjacent even through row breaks
    # NOTE: There are no parts line edges
    line_length = text.find("\n")
    data = text.translate(str.maketrans({"\n": ""}))
    for number in re.finditer(r"\d+", data):
        low, high = number.span()
        low, high = low - 1, high + 1
        above, bellow, before, after = False, False, False, False

        if low > line_length:
            tmp_a = data[low - line_length : high - line_length]
            above = tmp_a.count(".") != len(tmp_a)

        if high + line_length < len(data):
            tmp_b = data[low + line_length : high + line_length]
            bellow = tmp_b.count(".") != len(tmp_b)

        if low >= 0:
            before = "." != data[low]

        if high <= len(data):
            after = "." != data[high - 1]

        if above or bellow or before or after:
            yield int(number[0])


def to_kernel(i, row_length):
    """3x3 kernel"""
    yield i - 1
    yield i + 1
    yield from (i - row_length + k for k in (-1, 0, 1))
    yield from (i + row_length + k for k in (-1, 0, 1))


def part2(text):
    # NOTE: Part numbers are never adjacent even through row breaks
    # NOTE: There are no parts line edges
    # NOTE: We should be abe to do something smart for the number checks to just check the
    #       close by/possible neighbors. bisect on min(kernel) and mix(kernel) make this
    #       more efficient if data set would be bigger.
    numbers = tuple((int(m[0]), tuple(range(*m.span()))) for m in re.finditer(r"\d+", text))
    line = text.find("\n") + 1
    gears = (set(to_kernel(match.start(), line)) for match in re.finditer(r"\*", text))
    for gear in gears:
        gear_ratio = []
        for ratio, span in numbers:
            for r in span:
                if r in gear:
                    gear_ratio.append(ratio)
                    break
        try:
            yield mul(*gear_ratio)
        except TypeError:
            pass


print(f"{sum(part1(example))=}")
print(f"{sum(part1(validation))=}")

print(f"{sum(part2(example))=}")
print(f"{sum(part2(validation))=}")
