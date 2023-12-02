from pathlib import Path
from typing import NamedTuple, Self, Generator, Iterable

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
        return (
            self.red >= other.red
            and self.green >= other.green
            and self.blue >= other.blue
        )

    @classmethod
    def from_reveal(cls, reveal: str):
        items = (cube.partition(" ") for cube in reveal.split(", "))
        return cls(**{b: int(a) for a, _, b in items})

    @classmethod
    def max(cls, cubes: Iterable[Self]):
        red, green, blue = 0, 0, 0
        for obj in cubes:
            red = max(red, obj.red)
            green = max(green, obj.green)
            blue = max(blue, obj.blue)
        return cls(red=red, green=green, blue=blue)


def parse_game(line: str) -> tuple[int, Cube]:
    game, _, data = line.partition(": ")
    _, _, game_no = game.partition(" ")
    cubes = map(Cube.from_reveal, data.split("; "))
    return int(game_no), Cube.max(cubes)


def parse_games(text) -> Generator[tuple[int, Cube], None, None]:
    yield from map(parse_game, text.splitlines())


def part_1(games) -> int:
    threshold = Cube(red=12, green=13, blue=14)
    return sum(game for game, cube in games if threshold >= cube)


def part_2(games) -> int:
    return sum(cube.red * cube.green * cube.blue for _, cube in games)


example_games = list(parse_games(example))
validation_games = list(parse_games(validation))

print(f"{part_1(example_games)=}")
print(f"{part_1(validation_games)=}")

print(f"{part_2(example_games)=}")
print(f"{part_2(validation_games)=}")
