from string import ascii_letters
from pathlib import Path
import re

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()

example1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

example2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


def part1(data):
    trans = str.maketrans(dict.fromkeys(ascii_letters, ""))
    return sum(int(c[0] + c[-1]) for c in data.translate(trans).strip().splitlines())


def part2(data):
    trans = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    transex = re.compile(rf"(?=({'|'.join(trans.keys())}))")
    part1(transex.sub(lambda m: trans[m[1]], data))


part1(example1)
part1(validation)

part2(example2)
part2(validation)
