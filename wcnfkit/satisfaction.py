from typing import List


def clause_satisfied(clause_literals: List[int], assignment_str: str) -> bool:
    for lit in clause_literals:
        if lit > 0:
            var_index = lit - 1
            if assignment_str[var_index] == '1':
                return True
        else:
            var_index = abs(lit) - 1
            if assignment_str[var_index] == '0':
                return True
    return False


def count_satisfied_clauses(clauses: List[List[int]], assignment_str: str) -> int:
    count = 0
    for clause in clauses:
        if clause_satisfied(clause, assignment_str):
            count += 1
    return count


