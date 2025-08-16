from typing import List, Tuple


def parse_clause(clause_str: str) -> List[int]:
    tokens = clause_str.strip().split()
    results: List[int] = []
    for token in tokens[1:]:
        val = int(float(token))
        if val == 0:
            break
        results.append(val)
    return results


def parse_wdimacs(filename: str) -> Tuple[int, int, List[List[int]]]:
    n = 0
    m = 0
    clauses: List[List[int]] = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            if line.startswith('p'):
                parts = line.split()
                if len(parts) >= 4:
                    n = int(parts[2])
                    m = int(parts[3])
            else:
                clause_literals = parse_clause(line)
                clauses.append(clause_literals)
    return n, m, clauses


