from solver.types import ProblemDefinition, Solution


def get_problem_definition() -> ProblemDefinition:
    with open("instance.json", "r", encoding="utf-8") as file:
        return ProblemDefinition.model_validate_json(file.read())


def get_solution(solution_path: str) -> Solution:
    with open(solution_path, "r", encoding="utf-8") as file:
        return Solution.model_validate_json(file.read())
