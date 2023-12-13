from pathlib import Path
from typing import NamedTuple
import re
from itertools import batched

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".strip()


class Range(NamedTuple):
    start: int
    stop: int
    delta: int = 0

    def __contains__(self, value: int) -> bool:
        return self.start <= value < self.stop


def page2ranges(m):
    digits = re.compile(r"\d+")
    for stop, start, step in batched(map(int, digits.findall(m)), 3):
        yield Range(start, start + step, stop - start)


def parse_input(text):
    __seeds, *__almanac = text.split("\n\n")
    seeds = list(map(int, re.findall(r"\d+", __seeds)))

    almanac = {}
    for page in __almanac:
        __name, _, rest = page.partition(":")
        name = __name.replace("-", " ").split(" ")[-2]
        almanac[name] = sorted(page2ranges(rest))

    return seeds, almanac


def part1(data):
    seeds, almanac = data
    for seed in seeds:
        tmp = seed
        for page in almanac.values():
            for translation in page:
                if tmp in translation:
                    tmp += translation.delta
                    break
        yield tmp


def part2(data):
    __seeds, almanac = data
    seeds = [Range(start, start + n) for start, n in batched(__seeds, 2)]
    for page in almanac.values():
        tmp = []
        for current in seeds:
            rem = current
            for p in page:
                start, stop = rem.start in p, rem.stop in p
                if start and stop:
                    tmp.append(Range(rem.start + p.delta, rem.stop + p.delta))
                    break
                if start:
                    tmp.append(Range(rem.start + p.delta, p.stop + p.delta))
                    rem = Range(p.stop, rem.stop)
                if stop:
                    tmp.append(Range(rem.start, p.start))
                    tmp.append(Range(p.start + p.delta, rem.stop + p.delta))
            else:
                tmp.append(rem)
        seeds = tmp
    yield from seeds


example_data = parse_input(example)
validation_data = parse_input(validation)
print(min(part1(example_data)))
print(min(part1(validation_data)))

print(min(part2(example_data)).start)
print(min(part2(validation_data)).start)
