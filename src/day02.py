from pathlib import Path
from typing import NamedTuple, Self, Iterable
from collections import defaultdict
import re

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()

example = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip()


class Cube(NamedTuple):
    red: int = 0
    green: int = 0
    blue: int = 0

    def __ge__(self, other: Self) -> bool:
        return all(s >= o for s, o in zip(self, other, strict=True))

    @classmethod
    def from_game(cls, line: str):
        regex = re.compile(r"(\d+) (\w+)")
        dictionary = defaultdict(int)
        for n, color in regex.findall(line):
            dictionary[color] = max(dictionary[color], int(n))
        return cls(**dictionary)


def part_1(games: Iterable[Cube]) -> int:
    threshold = Cube(red=12, green=13, blue=14)
    return sum(n for n, cube in enumerate(games, start=1) if threshold >= cube)


def part_2(games: Iterable[Cube]) -> int:
    return sum(cube.red * cube.green * cube.blue for cube in games)


example_games = tuple(map(Cube.from_game, example.splitlines()))
validation_games = tuple(map(Cube.from_game, validation.splitlines()))

print(*enumerate(example_games, start=1), sep="\n")

print(f"{part_1(example_games)=}")
print(f"{part_1(validation_games)=}")

print(f"{part_2(example_games)=}")
print(f"{part_2(validation_games)=}")
