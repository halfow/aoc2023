from pathlib import Path
import re
from collections import defaultdict
from functools import reduce

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def parse(data: str) -> list[str]:
    return data.replace("\n", "").split(",")


def _hash(string: str):
    return reduce(lambda x, y: (x + ord(y)) * 17 % 256, string, 0)


def arrange_lenses(data: list[str]):
    regex = re.compile(r"(?P<label>[a-z]+)(?P<operation>[=-])(?P<value>[0-9]*)")
    table = defaultdict(list)

    for match in filter(None, map(regex.match, data)):
        label = match["label"]
        lens = label, match["value"]

        bucket = table[_hash(label)]

        n = next((x for x, (y, _) in enumerate(bucket) if y == label), -1)
        match (n, match["operation"]):
            case (-1, "="):
                bucket.append(lens)
            case (_, "="):
                bucket[n] = lens
            case (-1, "-"):
                pass
            case (_, "-"):
                bucket.pop(n)
    return table


def part2(text: str) -> int:
    return sum(
        (box + 1) * slot * int(value)
        for box, lenses in arrange_lenses(parse(text)).items()
        for slot, (_, value) in enumerate(lenses, start=1)
    )


print("part 1", sum(map(_hash, parse(validation))))
print("part 2", part2(validation))
