from pathlib import Path
from itertools import chain
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


step = {
    "|": lambda c, t: (t, Position(2 * t.y - c.y, t.x)),
    "-": lambda c, t: (t, Position(t.y, 2 * t.x - c.x)),
    "L": lambda c, t: (t, Position(t.y - c.x + t.x, t.x - c.y + t.y)),
    "J": lambda c, t: (t, Position(t.y + c.x - t.x, t.x + c.y - t.y)),
    "7": lambda c, t: (t, Position(t.y - c.x + t.x, t.x - c.y + t.y)),
    "F": lambda c, t: (t, Position(t.y + c.x - t.x, t.x + c.y - t.y)),
}


def parse(text: str) -> Generator[str, None, None]:
    yield from text.splitlines()


def start_points(plane: Sequence[str]) -> Generator[tuple[Position, Position], None, None]:
    start = next(Position(y, line.find("S")) for y, line in enumerate(plane) if "S" in line)
    points = (((0, 1), "-J7"), ((0, -1), "-FL"), ((-1, 0), "|F7"), ((1, 0), "|LJ"))
    _candidates = ((Position(start.y + y, start.x + x), d) for (y, x), d in points)
    x_max, y_max = len(plane[0]), len(plane)
    candidates = ((c, d) for c, d in _candidates if (0 <= c.x <= x_max) and (0 <= c.y <= y_max))
    yield from ((start, c) for c, d in candidates if plane[c.y][c.x] in d)


def loop_positions(text) -> set[Position]:
    plane = tuple(parse(text))
    data = list(start_points(plane))
    seen = set(chain.from_iterable(data))
    while data:
        tmp = []
        for c, t in data:
            a, b = step[plane[t.y][t.x]](c, t)
            if b not in seen:
                tmp.append((a, b))
                seen.add(b)
        data = tmp
    return seen


def part1(text: str) -> int:
    return len(loop_positions(text)) // 2


def part2(text: str) -> int:
    to_maze = str.maketrans({"F": "┌", "7": "┐", "L": "└", "J": "┘", "|": "│", "-": "─"})
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
        print("".join(string).translate(to_maze))
    return counter


print(f"{part1(example_1)=}")
print(f"{part1(example_2)=}")
print(f"{part1(validation)=}")

print(f"{part2(example_3)=}")
print(f"{part2(example_4)=}")
print(f"{part2(example_5)=}")
print(f"{part2(validation)=}")
