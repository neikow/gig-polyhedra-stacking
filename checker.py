from dataclasses import dataclass

from solver.importer import get_solution, get_problem_definition
from solver.shape_utils.polyhedron import point_inside_polyhedron
from solver.types import Placement, Piece, Point3D, ProblemDefinition, Solution
from utils.timer import with_timer


def get_transformed_vertices(placement: Placement, piece: Piece) -> list[Point3D]:
    faces = placement.transformed_faces(piece)
    vertices = []
    for face in faces:
        vertices.extend(face.get_vertices())
    return vertices


def get_pieces_vertices(solution: Solution, problem: ProblemDefinition) -> list[Point3D]:
    all_vertices = []
    for placement in solution.polyedres:
        piece = next(p for p in problem.pieces if p.index == placement.index)
        all_vertices.extend(get_transformed_vertices(placement, piece))

    return all_vertices


@dataclass
class CheckResult:
    are_inside: bool
    no_intersections: bool
    positive_volume: bool


def are_pieces_inside(solution: Solution, problem: ProblemDefinition) -> bool:
    res = True
    for vertex in get_pieces_vertices(solution, problem):
        if not point_inside_polyhedron(vertex, problem.polyhedron):
            print("Vertex outside polyhedron:", vertex)
            res = False

    return res


def no_intersections(solution: Solution, problem: ProblemDefinition) -> bool:
    pieces = problem.pieces
    placements = solution.polyedres
    for i in range(len(placements)):
        for j in range(i + 1, len(placements)):
            if placements[i].intersects(placements[j], pieces):
                print(f"Intersection between piece {placements[i].index} and piece {placements[j].index}")
                return False
    return True


@with_timer
def check_solution(sol_path: str) -> CheckResult:
    sol = get_solution(sol_path)
    prob = get_problem_definition()

    return CheckResult(
        are_inside=are_pieces_inside(sol, prob),
        no_intersections=no_intersections(sol, prob),
        positive_volume=sol.volume > 0,
    )


if __name__ == "__main__":
    result = check_solution("solution.json")
    print(result)
