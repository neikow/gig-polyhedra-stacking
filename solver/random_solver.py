import random

import matplotlib.pyplot as plt
import numpy as np

from solver.shape_utils.polyhedron import point_inside_polyhedron
from solver.types import ProblemDefinition, Solution, Polyhedron, Vector3D, Point3D, Quaternion, Placement
from solver.vizualizer import draw_container_polyhedron, draw_placement
from solver.volume_calculator import volume_polyhedrons_triangles
from utils.timer import with_timer

max_placement_attempts = 100
max_iterations = 100


def get_polyhedron_bounds(poly: Polyhedron) -> tuple[float, float, float, float, float, float]:
    min_x = min(vertex.x for vertex in poly.vertices)
    max_x = max(vertex.x for vertex in poly.vertices)
    min_y = min(vertex.y for vertex in poly.vertices)
    max_y = max(vertex.y for vertex in poly.vertices)
    min_z = min(vertex.z for vertex in poly.vertices)
    max_z = max(vertex.z for vertex in poly.vertices)
    return min_x, max_x, min_y, max_y, min_z, max_z


def random_position_inside_polyhedron(
        poly: Polyhedron,
        bounds: tuple[float, float, float, float, float, float]
) -> Vector3D:
    position = Point3D(x=np.inf, y=np.inf, z=np.inf)
    min_x, max_x, min_y, max_y, min_z, max_z = bounds

    while not point_inside_polyhedron(position, poly):
        position = Point3D(
            x=np.random.uniform(min_x, max_x),
            y=np.random.uniform(min_y, max_y),
            z=np.random.uniform(min_z, max_z)
        )

    return position.to_vector()


USE_DEBUG_VISUALIZATION = False


@with_timer
def solve_random(problem: ProblemDefinition) -> Solution:
    placed_pieces: list[Placement] = []
    pieces = problem.pieces
    it = 0

    bounds = get_polyhedron_bounds(problem.polyhedron)

    while True:
        n = len(placed_pieces)
        it += 1
        print("Iteration", it, " - placed pieces:", n)

        if it > max_iterations:
            print("Max iterations reached, stopping. ")
            break

        piece = pieces[random.randint(0, len(pieces) - 1)]

        placed_piece: Placement | None = None
        for attempt in range(max_placement_attempts):
            position = random_position_inside_polyhedron(problem.polyhedron, bounds)
            quaternion = Quaternion(
                s=random.uniform(0, 1),
                u=Vector3D(
                    x=random.uniform(0, 1),
                    y=random.uniform(0, 1),
                    z=random.uniform(0, 1)
                ).normalize()
            )

            maybe_placed_piece = Placement(
                index=piece.index,
                vecteur=position,
                quaternion=quaternion
            )

            faces = maybe_placed_piece.transformed_faces(piece)

            if any(
                    not point_inside_polyhedron(problem_vertex := vertex, problem.polyhedron)
                    for face in faces for vertex in face.get_vertices()
            ):
                print(
                    f"Piece {piece.index} out of bounds"
                )

                if USE_DEBUG_VISUALIZATION:
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')

                    draw_container_polyhedron(ax, problem.polyhedron)
                    draw_placement(ax, maybe_placed_piece, piece)

                    ax.scatter3D(problem_vertex.x, problem_vertex.y, problem_vertex.z, color='r', s=100)

                    plt.show()
                continue

            intersect_other: Placement | None = None

            if any(
                    maybe_placed_piece.intersects(intersect_other := other, pieces)
                    for other in placed_pieces
            ):
                print(
                    f"Piece {piece.index} intersects with already placed piece ({intersect_other.index})"
                )

                if USE_DEBUG_VISUALIZATION:
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')

                    draw_placement(ax, maybe_placed_piece, piece)
                    other_piece = next(p for p in pieces if p.index == intersect_other.index)
                    draw_placement(ax, intersect_other, other_piece)

                    plt.show()
                continue

            placed_piece = maybe_placed_piece
            break

        if placed_piece is not None:
            placed_pieces.append(placed_piece)
        else:
            placed_pieces.pop()

    return Solution(
        polyedres=placed_pieces,
        volume=volume_polyhedrons_triangles(placed_pieces, pieces)
    )
