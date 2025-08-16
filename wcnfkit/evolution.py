import random
import time
from typing import List, Tuple

from .satisfaction import count_satisfied_clauses, clause_satisfied


def random_assignment(num_variables: int) -> str:
    return ''.join(random.choice('01') for _ in range(num_variables))


def crossover(parent1: str, parent2: str) -> Tuple[str, str]:
    n = len(parent1)
    point = random.randint(1, n - 1) if n > 1 else 1
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(bitstring: str, pmut: float = 0.01) -> str:
    lst = list(bitstring)
    for i in range(len(lst)):
        if random.random() < pmut:
            lst[i] = '0' if lst[i] == '1' else '1'
    return ''.join(lst)


def compute_unsatisfied_clauses(clauses: List[List[int]], assignment_str: str) -> List[List[int]]:
    unsatisfied: List[List[int]] = []
    for clause in clauses:
        if not clause_satisfied(clause, assignment_str):
            unsatisfied.append(clause)
    return unsatisfied


def compute_r3(assignment_str: str, weights: List[int]) -> float:
    numerator = 0
    denominator = 1
    for j, bit in enumerate(assignment_str):
        k_sign = +1 if bit == '1' else -1
        numerator += k_sign * weights[j]
        denominator += abs(weights[j])
    return 0.5 * (1 + (numerator / denominator))


def update_weights(weights: List[int], best_assignment_str: str) -> List[int]:
    for j, bit in enumerate(best_assignment_str):
        k_sign = +1 if bit == '1' else -1
        weights[j] -= k_sign
    return weights


def evolutionary_search(clauses: List[List[int]], n: int, m: int, time_budget: float, repetitions: int) -> List[Tuple[int, int, str]]:
    population_size = 20
    p_m = 1.0 / n if n > 0 else 0.01
    alpha = 1

    results: List[Tuple[int, int, str]] = []

    for _ in range(repetitions):
        start_time = time.time()
        weights = [0] * n
        population = [random_assignment(n) for _ in range(population_size)]

        def refined_fitness(assign_str: str) -> float:
            fval = count_satisfied_clauses(clauses, assign_str)
            r_val = compute_r3(assign_str, weights)
            return fval + alpha * r_val

        fitness_values = [refined_fitness(ind) for ind in population]

        best_solution = None
        best_f_base = -1
        best_refined = -1
        generation_count = 0

        while True:
            if (time.time() - start_time) >= time_budget:
                break

            generation_count += 1

            new_population: List[str] = []
            new_fitness_vals: List[float] = []

            while len(new_population) < population_size:
                idx1, idx2 = random.sample(range(population_size), 2)
                p1 = population[idx1] if fitness_values[idx1] > fitness_values[idx2] else population[idx2]

                idx3, idx4 = random.sample(range(population_size), 2)
                p2 = population[idx3] if fitness_values[idx3] > fitness_values[idx4] else population[idx4]

                c1, c2 = crossover(p1, p2)
                c1 = mutate(c1, p_m)
                c2 = mutate(c2, p_m)

                new_population.append(c1)
                new_population.append(c2)
                new_fitness_vals.append(refined_fitness(c1))
                new_fitness_vals.append(refined_fitness(c2))

            population = new_population[:population_size]
            fitness_values = new_fitness_vals[:population_size]

            best_index = max(range(population_size), key=lambda i: fitness_values[i])
            best_individual = population[best_index]
            best_val_refined = fitness_values[best_index]
            best_val_base = count_satisfied_clauses(clauses, best_individual)

            if best_val_refined > best_refined:
                best_refined = best_val_refined
                best_solution = best_individual
                best_f_base = best_val_base

            update_weights(weights, best_individual)

            if best_f_base == m:
                break

        evaluations = generation_count * population_size
        results.append((evaluations, best_f_base, best_solution or ''))

    return results


