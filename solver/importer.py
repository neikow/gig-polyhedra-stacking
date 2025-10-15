from solver.types import ProblemDefinition


def get_problem_definition() -> ProblemDefinition:
    with open("instance.json", "r", encoding="utf-8") as file:
        return ProblemDefinition.model_validate_json(file.read())