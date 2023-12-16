from pathlib import Path
import re
from itertools import product, pairwise

file_name = Path(__file__).with_suffix(".txt").name
dir_name = Path(__file__).parent.with_name("input")
validation = (dir_name / file_name).read_text()
example = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""".strip()


def parse(text: str):
    for line in text.splitlines():
        springs, pattern = line.split()
        yield (
            springs,
            tuple(map(int, pattern.split(","))),
        )


def recurse(spring, sequence):
    return {
        s: tuple(
            (m.start(), m.start() + s)
            for m in re.finditer(rf"(?=([#?]{{{s}}}))", spring)
        )
        for s in set(sequence)
    }


def part1(text: str):
    for spring, sequence in parse(text):
        possible = recurse(spring, sequence)
        # TODO: we know some min and max boundaries of the sequence
        #       this can be used to reduce the search space.
        #       Further more we can rely on the fact that all "#"
        #       always have to be covered by the sequence.
        #       Some can be full cover or false. This will reduce
        #       the search space even more.
        #       for a sequence of "#" we can assume that N-1 "#" can
        #       be reduced and all ranges touching the "#" boundary
        #       can be removed. eg "##" at 5,7 -> "#" in range 4, 8
        #       can be removed as candidate solution
        for c in product(*(possible[s] for s in sequence)):
            if "#" in spring[: c[0][0]] or "#" in spring[c[-1][1] :]:
                continue
            for (_, a), (b, _) in pairwise(c):
                if a >= b:
                    break
                if "#" in spring[a:b]:
                    break
            else:
                yield True


print(sum(part1(example)))
print(sum(part1(validation)))
