import csv
from dataclasses import dataclass
import itertools
import os
from typing import Iterable

from common import CLASS_PATH


@dataclass
class Assignment:
    path: str
    output: str
    suffix_length: int
    questions: list[str]


def pset_questions(num: str) -> Iterable:
    if num == "5":
        return (x for x in range(1, 12+1) if x != 4)
    elif num == "6":
        return range(1, 13+1)
    elif num == "7-1":
        return range(1, 15+1)
    elif num == "7-2":
        return range(1, 14+1)
    elif num == "7-3":
        return range(1, 11+1)

    raise NotImplementedError("Invalid pset #")


def problem_set(num: str) -> Assignment:
    folder = os.path.join(CLASS_PATH, f"Problem Set {num}")
    questions = [str(q) for q in pset_questions(num)]

    return Assignment(path=os.path.join(folder, f"ps{num}.txt"), output=os.path.join(folder, f"ps{num}.csv"),
                      suffix_length=len(f"quantumintro__HW{num}_Q"), questions=questions)


def quiz2() -> Assignment:
    folder = os.path.join(CLASS_PATH, f"Quiz 2")

    return Assignment(path=os.path.join(folder, f"quiz2.txt"), output=os.path.join(folder, f"quiz2.csv"),
                      suffix_length=len(f"quantumintro__Quiz2_"), questions=[str(q) for q in range(1, 17)])


def final() -> Assignment:
    folder = os.path.join(CLASS_PATH, f"Final")

    return Assignment(path=os.path.join(folder, f"final.txt"), output=os.path.join(folder, f"final.csv"),
                      suffix_length=len(f"quantumintro__Final_"), questions=[f"{q:02}" for q in range(1, 35)])


def process_grades(assign: Assignment):
    with open(assign.path) as f:
        lines = [l.strip() for l in f.readlines()]

    # header, divider
    lines.pop(0)
    lines.pop(0)

    grades: dict[str, dict[str, float]] = {}

    while len(lines) > 0:
        line = lines.pop(0)

        parts = line.replace(" ", "").split("|")

        if len(parts) < 5:
            break

        if parts[0] == '':
            continue

        if parts[0] not in grades:
            grades[parts[0]] = {}

        grades[parts[0]][parts[2][assign.suffix_length:]] = float(parts[3])

    with open(assign.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sid"] + [str(q) for q in assign.questions])
        for sid in grades:
            writer.writerow([sid] + [f"{grades[sid][str(q)]:.3f}" if str(q)
                            in grades[sid] else 0 for q in assign.questions])
