from pathlib import Path
import re
from math import prod

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = """
Time:      7  15   30
Distance:  9  40  200
""".strip()


def parse(text):
    digits = re.compile(r"\d+")
    data = list(map(int, digits.findall(text)))
    mid = len(data) // 2
    return zip(data[:mid], data[mid:])


def part(text: str):
    for ms, mm in parse(text):
        yield sum((x * y) > mm for x, y in zip(range(1, ms), range(ms - 1, 0, -1)))


print(f"Part 1: {prod(part(example)):>10}")
print(f"Part 1: {prod(part(validation)):>10}")
print(f"Part 2: {prod(part(example.replace(" ", ""))):>10}")
print(f"Part 2: {prod(part(validation.replace(" ", ""))):>10}")
