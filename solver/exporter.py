from solver.types import Solution


def save_solution(path: str, solution: Solution) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write(solution.model_dump_json(indent=4))
