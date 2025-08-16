import sys
import random

from wcnfkit.satisfaction import clause_satisfied, count_satisfied_clauses
from wcnfkit.wdimacs import parse_clause, parse_wdimacs
from wcnfkit.evolution import evolutionary_search


def task1(clause_str, assignment_str):
    clause_literals = parse_clause(clause_str)
    print(1 if clause_satisfied(clause_literals, assignment_str) else 0)


def task2(wdimacs_file, assignment_str):
    n, m, clauses = parse_wdimacs(wdimacs_file)
    correct_num = count_satisfied_clauses(clauses, assignment_str)
    print(correct_num)


def task3(wdimacs_file, time_budget, repetitions):
    n, m, clauses = parse_wdimacs(wdimacs_file)
    results = evolutionary_search(clauses, n, m, time_budget, repetitions)
    for evaluations, best_f_base, best_solution in results:
        print(f"{evaluations}\t{best_f_base}\t{best_solution}")


def main():
    random.seed(24)

    question_arg = sys.argv[sys.argv.index("-question") + 1] if "-question" in sys.argv else ""
    question_num = int(question_arg) if question_arg else 0

    if question_num == 1:
        assignment_arg = sys.argv[sys.argv.index("-assignment") + 1] if "-assignment" in sys.argv else ""
        clause_arg = sys.argv[sys.argv.index("-clause") + 1] if "-clause" in sys.argv else ""
        task1(clause_arg, assignment_arg)

    elif question_num == 2:
        assignment_arg = sys.argv[sys.argv.index("-assignment") + 1] if "-assignment" in sys.argv else ""
        wdimacs_arg = sys.argv[sys.argv.index("-wdimacs") + 1] if "-wdimacs" in sys.argv else ""
        task2(wdimacs_arg, assignment_arg)

    elif question_num == 3:
        wdimacs_arg = sys.argv[sys.argv.index("-wdimacs") + 1] if "-wdimacs" in sys.argv else ""
        time_budget_arg = sys.argv[sys.argv.index("-time_budget") + 1] if "-time_budget" in sys.argv else ""
        repetitions_arg = sys.argv[sys.argv.index("-repetitions") + 1] if "-repetitions" in sys.argv else ""
        task3(wdimacs_arg, float(time_budget_arg), int(repetitions_arg))


if __name__ == "__main__":
    main()

