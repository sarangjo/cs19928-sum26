import csv
import os


def _folder(num):
    return os.path.join("C:\\", "Users", "saran", "Box",
                        "CMSC 19928-30 Summer 2026", f"Problem Set {num}")


def _path(num):
    return os.path.join(_folder(num), f"ps{num}.txt")


def _output(num):
    return os.path.join(_folder(num), f"ps{num}.csv")


def _suffix_length(num):
    return len(f"quantumintro__HW{num}_Q")


def _questions(num):
    if num == 5:
        return list(range(1, 3)) + list(range(5, 13))
    elif num == 6:
        return list(range(1, 14))

    return []


def process_grades(pset_num):
    with open(_path(pset_num)) as f:
        lines = [l.strip() for l in f.readlines()]

    # header, divider
    lines.pop(0)
    lines.pop(0)

    grades: dict[str, dict[str, int]] = {}

    while len(lines) > 0:
        line = lines.pop(0)

        parts = line.replace(" ", "").split("|")

        if len(parts) < 5:
            break

        if parts[0] not in grades:
            grades[parts[0]] = {}

        grades[parts[0]][parts[2][_suffix_length(pset_num):]] = int(parts[3])

    # print(grades)

    with open(_output(pset_num), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sid"] + [str(q) for q in _questions(pset_num)])
        for sid in grades:
            writer.writerow([sid] + [grades[sid][str(q)] if str(q)
                            in grades[sid] else 0 for q in _questions(pset_num)])
