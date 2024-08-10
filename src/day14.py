from pathlib import Path
from typing import Iterable
from io import StringIO


file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".strip()


def parse(data: str) -> tuple[str, ...]:
    return tuple(line for line in data.splitlines())


def transpose(grid: Iterable[str]) -> tuple[str, ...]:
    return tuple(zip(*grid))


def fall(column: Iterable[str]) -> str:
    """Simulate falling of the O tiles"""
    update = StringIO()
    ball = empty = 0
    for symbol in column:
        match symbol:
            case ".":
                empty += 1
            case "O":
                ball += 1
            case "#":
                update.write("O" * ball)
                update.write("." * empty)
                update.write("#")
                ball = empty = 0
    update.write("O" * ball)
    update.write("." * empty)
    return update.getvalue()


def north(grid: tuple[str, ...]) -> tuple[str, ...]:
    return transpose(fall(col) for col in transpose(grid))


def west(grid: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(fall(col) for col in grid)


def south(grid: tuple[str, ...]) -> tuple[str, ...]:
    return transpose(fall(reversed(col))[::-1] for col in transpose(grid))


def east(grid: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(fall(reversed(col))[::-1] for col in grid)


def cycle(grid):
    """Rotate the grid a full cycle"""
    for move in (north, west, south, east):
        grid = move(grid)
    return grid


def part2(grid):
    n, seen = 0, []

    while grid not in seen:  # Assume cycle exists and quite short.
        seen.append(grid)  # Can be complimented with a O(1) lookup. If cycle is long.
        grid = cycle(grid)
        n += 1

    cycle_start = seen.index(grid)
    cycle_length = n - cycle_start
    cycles_remaining = 1_000_000_000 - cycle_start
    return seen[cycle_start + (cycles_remaining % cycle_length)]


def points(grid: tuple[str, ...]):
    for row, score in zip(grid, range(len(grid), 0, -1)):
        yield row.count("O") * score


print("part 1:", sum(points(north(parse(validation)))))
print("part 2:", sum(points(part2(parse(validation)))))
