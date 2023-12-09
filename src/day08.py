from pathlib import Path
from itertools import cycle
from math import lcm
import re
from typing import Generator, Any

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example_1 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".strip()

example_2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".strip()

example_3 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".strip()


def parse(text: str):
    pattern, __instructions = text.split("\n\n")
    instructions = re.findall(r"(\w+) = \((\w+), (\w+)\)", __instructions)
    return tuple(map("LR".find, pattern)), {a: b for a, *b in instructions}


def walk(text) -> Generator[int, Any, Any]:
    step, chart = parse(text)

    def sub_walk(start) -> int:
        current = start
        for n, i in enumerate(cycle(step), start=1):
            current = chart[current][i]
            if current.endswith("Z"):
                return n
        raise  # NOTE: Just for type checker

    starts = sorted(c for c in chart.keys() if c.endswith("A"))
    yield from map(sub_walk, starts)


print(f"Part 1: {next(walk(validation)):>16}")
print(f"Part 2: {lcm(*walk(validation)):>16}")
