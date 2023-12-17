from pathlib import Path
from functools import lru_cache

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""".strip()


def parse(text: str):
    for line in text.splitlines():
        springs, pattern = line.split()
        yield (springs, tuple(map(int, pattern.split(","))))


@lru_cache(typed=True)
def walk(row, segments) -> int:
    # Handle for no more recursion
    if not row:
        return int(not segments)
    elif not segments:
        return int("#" not in row)

    # Handle for current character
    match character := row[0]:
        case ".":  # try next and return
            return walk(row[1:], segments)
        case "?":  # possible sequence break
            result = walk(row[1:], segments)
        case "#":  # sequence break
            result = 0
        case _:
            raise ValueError(f"Unknown character {character}")

    # Handle for current segment
    segment = segments[0]  # Current segment length
    try:
        if "." in row[:segment]:  # Segment is broken
            pass
        elif segment == len(row):  # Segment fits
            return result + walk(row[segment + 1 :], segments[1:])
        elif row[segment] != "#":  # Segment is not to long
            return result + walk(row[segment + 1 :], segments[1:])
    except IndexError:
        pass
    return result


def part1(text: str):
    return sum(walk(a, b) for a, b in parse(text))


def part2(text: str):
    return sum(walk("?".join((a,) * 5), b * 5) for a, b in parse(text))


print(f"{part1(example)=}")
print(f"{part1(validation)=}")

print(f"{part2(example)=}")
print(f"{part2(validation)=}")
