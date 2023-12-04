from pathlib import Path
import re
from collections import deque

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".strip()


def party(text: str):
    digits = re.compile(r"\d+")
    for line in text.splitlines():
        card, _, numbers = line.partition(" | ")
        _, _, ticket = card.partition(": ")
        yield len(set(digits.findall(ticket)).intersection(digits.findall(numbers)))


def part1(game_matches):
    return ((2**i) // 2 for i in game_matches)


def part2(game_matches, no_numbers):
    stack = deque([1] * no_numbers, maxlen=no_numbers)
    for wins in game_matches:
        no_tickets = stack.popleft()
        stack.append(1)
        for n in range(wins):
            stack[n] += no_tickets
        yield no_tickets


example_data = list(party(example))
validation_data = list(party(validation))

print(f"{sum(part1(example_data))}")
print(f"{sum(part1(validation_data))}")

print(f"{sum(part2(example_data, 5))}")
print(f"{sum(part2(validation_data, 10))}")
