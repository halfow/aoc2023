import webbrowser
from requests import Session
from http import HTTPStatus
from os import environ
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

aoc = Session()
aoc.cookies.set("session", environ["SESSION"])

site = "https://adventofcode.com"
year = 2023

start = """
from pathlib import Path

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = \"""
\""".strip()
""".lstrip()


def get(day):
    response = aoc.get(f"{site}/{year}/day/{day}/input")
    root = Path(__file__)
    if response.status_code == HTTPStatus.OK:
        (root.with_name("input") / f"day{day:>02}.txt").write_text(response.text)
        (root.with_name("src") / f"day{day:>02}.py").write_text(start)


def web(day):
    webbrowser.open(f"{site}/{year}/day/{day}")


def submit(day, part, answer):
    if part not in (1, 2):
        raise ValueError(f"Expected 1 or 2, got {part}")
    print(aoc.post(f"{site}/{year}/day/{day}/answer", data={"level": part, "answer": answer}).text)


if __name__ == "__main__":
    from argparse import ArgumentParser
    from datetime import date

    parser = ArgumentParser()
    parser.add_argument(
        *("-d", "--day"),
        help="day to get (Default: %(default)s)",
        type=int,
        default=date.today().day,
    )
    args = parser.parse_args()

    web(args.day)
    get(args.day)
