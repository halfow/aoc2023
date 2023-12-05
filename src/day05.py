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


class Field(NamedTuple):
    start: int
    stop: int
    delta: int


def prutt(m):
    digits = re.compile(r"\d+")
    for stop, start, step in batched(map(int, digits.findall(m)), 3):
        yield Field(start, start + step, stop - start)


def party(text):
    seeds, *raw_almanac = text.split("\n\n")
    seeds = list(map(int, re.findall(r"\d+", seeds)))

    almanac = {}
    for maps in raw_almanac:
        name, _, rest = maps.partition(":")
        name = name.replace("-", " ").split(" ")[-2]
        almanac[name] = sorted(prutt(rest))

    return seeds, almanac


def part1(data):
    seeds, almanac = data
    for seed in seeds:
        tmp = seed
        for instructions in almanac.values():
            for lot in instructions:
                if tmp in range(lot.start, lot.stop):
                    tmp += lot.delta
                    break
        yield tmp


def part2(data):
    raw_seeds, almanac = data
    seeds = [range(start, start + n) for start, n in batched(raw_seeds, 2)]
    for mapping in almanac.values():
        tmp = []
        for current in seeds:
            remaining = current
            for lot in mapping:
                start = lot.start <= remaining.start < lot.stop
                stop = lot.start <= remaining.stop < lot.stop

                if start and stop:
                    tmp.append(range(remaining.start + lot.delta, remaining.stop + lot.delta))
                    break

                if start:
                    tmp.append(range(remaining.start + lot.delta, lot.stop + lot.delta))
                    remaining = range(lot.stop, remaining.stop)

                if stop:
                    tmp.append(range(remaining.start, lot.start))
                    tmp.append(range(lot.start + lot.delta, remaining.stop + lot.delta))
            else:
                tmp.append(remaining)
        seeds = tmp
    yield from seeds


example_data = party(example)
validation_data = party(validation)
print(min(part1(example_data)))
print(min(part1(validation_data)))

print(min(part2(example_data), key=lambda x: x.start).start)
print(min(part2(validation_data), key=lambda x: x.start).start)
