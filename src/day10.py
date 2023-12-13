from pathlib import Path
from typing import NamedTuple, Generator, Sequence

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example_1 = """
.....
.S-7.
.|.|.
.L-J.
.....
""".strip()

example_2 = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""".strip()

example_3 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""".strip()

example_4 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""".strip()

example_5 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".strip()


class Position(NamedTuple):
    y: int
    x: int


def parse(text: str) -> Generator[str, None, None]:
    yield from text.splitlines()


def start_points(
    plane: Sequence[str],
) -> Generator[tuple[Position, Position], None, None]:
    start = next(Position(y, x.find("S")) for y, x in enumerate(plane) if "S" in x)
    start_deltas = (
        (Position(0, 1), "-J7"),  # Right
        (Position(0, -1), "-FL"),  # Left
        (Position(-1, 0), "|F7"),  # Up
        (Position(1, 0), "|LJ"),  # Down
    )
    possible_connections = (
        (Position(start.y + move.y, start.x + move.x), valid)
        for move, valid in start_deltas
    )
    yield from (
        (start, move)
        for move, valid in possible_connections
        if plane[move.y][move.x] in valid
    )


def loop_positions(text) -> set[Position]:
    plane = tuple(parse(text))
    p, c = next(start_points(plane))
    seen = {p, c}
    while True:
        match plane[c.y][c.x]:
            case "|" | "-":
                p, c = c, Position(2 * c.y - p.y, 2 * c.x - p.x)
            case "L" | "7":
                p, c = c, Position(c.y - p.x + c.x, c.x - p.y + c.y)
            case "F" | "J":
                p, c = c, Position(c.y + p.x - c.x, c.x + p.y - c.y)
            case _:
                return seen
        seen.add(c)


def part1(text: str) -> int:
    return len(loop_positions(text)) // 2


def part2(text: str) -> int:
    maze = str.maketrans({"F": "┌", "7": "┐", "L": "└", "J": "┘", "|": "│", "-": "─"})
    loop = loop_positions(text)

    counter, pipe = 0, "|"
    for y, line in enumerate(parse(text)):
        inside = False
        string = [" "] * len(line)
        for x, c in enumerate(line):
            if (y, x) in loop:
                string[x] = c
                if c in pipe:
                    inside = not inside
                if c in "FL7J|":
                    pipe = {"F": "J|", "L": "7|"}.get(c, "|")
            elif inside:
                string[x] = "*"
                counter += 1
        print("".join(string).translate(maze))
    return counter


print(f"{part1(example_1)=}")
print(f"{part1(example_2)=}")
print(f"{part1(validation)=}")

print(f"{part2(example_3)=}")
print(f"{part2(example_4)=}")
print(f"{part2(example_5)=}")
print(f"{part2(validation)=}")
