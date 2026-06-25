#!/usr/bin/env python3

import csv
import datetime
import os
from typing import Any

QUIZ_1_PATH = os.path.join("C:\\", "Users", "saran", "Box",
                           "CMSC 19928-30 Summer 2026", "Student Data", "Quiz 1")

AUTOGRADABLE = set([
    1, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20
])
CODE = set([18])
QUESTIONS = list(range(1, 6)) + ["6a", "6b", "7a", "7b", "8a", "8b"] + list(range(9, 21))

FULL_GRADES = "Quiz1Final.csv"


def get_student_responses(question_num: str):
    """
    Returns a dictionary mapping student ID's to their latest response.
    """

    student_all_responses: dict[str, list[dict[str, Any]]] = {}
    with open(os.path.join(QUIZ_1_PATH, f"{question_num}.csv")) as f:
        reader = csv.DictReader(f)

        for line in reader:
            sid: str = line["sid"]

            if sid not in student_all_responses:
                student_all_responses[sid] = []

            student_all_responses[sid].append(line)

    # 2026-06-22 14:53:25.360875
    student_final_responses = {
        sid: sorted(student_all_responses[sid], key=lambda entry: datetime.datetime.strptime(
            entry["timestamp"], "%Y-%m-%d %H:%M:%S.%f"))[-1]
        for sid in student_all_responses
    }

    return student_final_responses


def process_autogradable(question_num: str, student_grades: dict[str, dict[str, Any]]):
    student_final_responses = get_student_responses(question_num)

    for sid in student_final_responses:
        if sid not in student_grades:
            student_grades[sid] = {}

        student_grades[sid][question_num] = f"{float(student_final_responses[sid]["percent"]):.4f}"


def process_non_autogradable(question_num: str, field="answer"):
    student_final_responses = get_student_responses(question_num)

    # The - 1'th item is the answer we want to grade
    with open(os.path.join(QUIZ_1_PATH, f"{question_num}-last.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, ["sid", "answer"])
        writer.writeheader()

        writer.writerows(
            sorted([
                {
                    "sid": sid,
                    "answer": student_final_responses[sid][field]
                }
                for sid in student_final_responses
            ], key=lambda l: l["sid"].lower())
        )


def setup_autograded():
    student_grades = {}

    for question_num in QUESTIONS:
        if question_num in AUTOGRADABLE:
            process_autogradable(str(question_num), student_grades)
        else:
            for sid in student_grades:
                student_grades[sid][question_num] = ""

    for sid in student_grades:
        student_grades[sid]["sid"] = sid

    with open(os.path.join(QUIZ_1_PATH, FULL_GRADES), "w", newline="") as f:
        writer = csv.DictWriter(f, ["sid"] + list(range(1, 21)))
        writer.writeheader()

        writer.writerows(
            [
                student_grades[sid] for sid in student_grades
            ]
        )


def main():
    for question_num in QUESTIONS:
        if question_num not in AUTOGRADABLE:
            print("processing:", question_num)
            try:
                process_non_autogradable(
                    str(question_num), field="code" if question_num in CODE else "answer")
            except:
                print("failed to process.")


if __name__ == "__main__":
    main()
