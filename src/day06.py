from pathlib import Path
import re
from math import prod, isqrt

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


def part1(text: str):
    for time, distance in parse(text):
        yield sum(
            (x * y) > distance
            for x, y in zip(
                range(1, time),
                range(time - 1, 0, -1),
            )
        )


def part2(text):
    for time, distance in parse(text):
        return isqrt(time**2 - 4 * distance)


print(f"Part 1: {prod(part1(example)):>10}")
print(f"Part 1: {prod(part1(validation)):>10}")

print(f"Part 2: {part2(example.replace(' ', '')):>10}")
print(f"Part 2: {part2(validation.replace(' ', '')):>10}")
