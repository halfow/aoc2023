from pathlib import Path
from collections import Counter
import re

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".strip()


def parse(text):
    data = iter(re.split(r"\s+", text))
    yield from zip(data, data)


def part1(text):
    weight = "AKQJT98765432"[::-1]
    for draw, bet in parse(text):
        hand = sorted(Counter(draw).values(), reverse=True)
        high = tuple(map(weight.find, draw))
        yield hand, high, int(bet)


def part2(text):
    weight = "AKQT98765432J"[::-1]
    for draw, bet in parse(text):
        try:
            ((char, _),) = Counter(draw.replace("J", "")).most_common(1)
            handy = draw.replace("J", char)
        except ValueError:
            handy = draw
        hand = sorted(Counter(handy).values(), reverse=True)
        high = tuple(map(weight.find, draw))
        yield hand, high, int(bet)


def calc(part, text):
    ranks = enumerate(sorted(part(text)), start=1)
    return sum(rank * bet for rank, (_, _, bet) in ranks)


print(f"{calc(part1, example)=}")
print(f"{calc(part1, validation)=}")

print(f"{calc(part2, example)=}")
print(f"{calc(part2, validation)=}")
