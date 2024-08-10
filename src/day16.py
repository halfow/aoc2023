from pathlib import Path
from typing import NamedTuple
from itertools import chain

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""".strip()


class Beam(NamedTuple):
    x: int = -1
    y: int = 0
    dx: int = 1
    dy: int = 0


def to_grid(string: str) -> list[list[str]]:
    return [list(row) for row in string.splitlines()]


def energize(grid: list[list[str]], start: Beam = Beam()) -> int:  # noqa: B008
    x, y = len(grid[0]), len(grid)
    beams = [start]
    seen = set()

    while beams:
        old = beams.pop()
        new = Beam(x=old.x + old.dx, y=old.y + old.dy, dx=old.dx, dy=old.dy)

        if new in seen or not (0 <= new.x < x) or not (0 <= new.y < y):
            continue

        seen.add(new)

        match grid[new.y][new.x]:
            case "|" if new.dx != 0:
                beams.append(Beam(x=new.x, y=new.y, dx=0, dy=-1))
                beams.append(Beam(x=new.x, y=new.y, dx=0, dy=1))
            case "-" if new.dy != 0:
                beams.append(Beam(x=new.x, y=new.y, dx=-1, dy=0))
                beams.append(Beam(x=new.x, y=new.y, dx=1, dy=0))
            case "/":
                beams.append(Beam(x=new.x, y=new.y, dx=-new.dy, dy=-new.dx))
            case "\\":
                beams.append(Beam(x=new.x, y=new.y, dx=new.dy, dy=new.dx))
            case _:
                beams.append(new)

    return len({(x, y) for x, y, *_ in seen})


def eval_frame(string: str) -> int:
    grid = to_grid(string)
    x, y = len(grid[0]), len(grid)

    starts = chain(
        (Beam(x=i, y=-1, dx=0, dy=1) for i in range(x)),  # first row
        (Beam(x=i, y=y, dx=0, dy=-1) for i in range(x)),  # last row
        (Beam(x=-1, y=i, dx=1, dy=0) for i in range(y)),  # first column
        (Beam(x=x, y=i, dx=-1, dy=0) for i in range(y)),  # last column
    )
    return max(map(lambda start: energize(grid, start), starts))


print("Part 1:", energize(to_grid(validation)))
print("Part 2:", eval_frame(validation))
