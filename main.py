from collections.abc import Callable
from typing import Literal

from solver.exporter import save_solution
from solver.importer import get_problem_definition, get_solution
from solver.random_solver import solve_random
from solver.types import ProblemDefinition, Solution
from solver.vizualizer import visualize_solution

algorithms: dict[str, Callable[[ProblemDefinition], Solution]] = {
    'random': solve_random,
}


def get_or_create_solution(
        problem_definition: ProblemDefinition,
        algorithm: Literal['random'],
        force_recompute: bool = False
) -> Solution:
    solution_path = f"solution_{algorithm}.json"

    alg = algorithms.get(algorithm)
    if alg is None:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    if force_recompute:
        sol = alg(problem_definition)
        save_solution(solution_path, sol)
    else:
        try:
            sol = get_solution(solution_path)
        except FileNotFoundError:
            sol = alg(problem_definition)
            save_solution(solution_path, sol)
    return sol


if __name__ == "__main__":
    problem = get_problem_definition()

    solution = get_or_create_solution(
        problem,
        algorithm='random',
        force_recompute=False
    )

    visualize_solution(problem, solution)
