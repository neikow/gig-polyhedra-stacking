import random

import numpy as np

from solver.shape_utils.polyhedron import point_inside_polyhedron
from solver.types import ProblemDefinition, Solution, Polyhedron, Vector3D, Point3D, Quaternion, Placement
from utils.timer import with_timer

max_placement_attempts = 50
max_iterations = 1000


def random_position_inside_polyhedron(poly: Polyhedron) -> Vector3D:
    position = Point3D(x=np.inf, y=np.inf, z=np.inf)
    min_x = min(vertex.x for vertex in poly.vertices)
    max_x = max(vertex.x for vertex in poly.vertices)
    min_y = min(vertex.y for vertex in poly.vertices)
    max_y = max(vertex.y for vertex in poly.vertices)
    min_z = min(vertex.z for vertex in poly.vertices)
    max_z = max(vertex.z for vertex in poly.vertices)

    while not point_inside_polyhedron(position, poly):
        position = Point3D(
            x=np.random.uniform(min_x, max_x),
            y=np.random.uniform(min_y, max_y),
            z=np.random.uniform(min_z, max_z)
        )

    return position.to_vector()


@with_timer
def solve_random(problem: ProblemDefinition) -> Solution:
    placed_pieces: list[Placement] = []
    pieces = problem.pieces
    it = 0
    while (n := len(placed_pieces)) < len(pieces):
        it += 1
        print("Iteration", it, " - placed pieces:", n, "/", len(pieces))

        if it > max_iterations:
            print(f"Reached max iterations ({max_iterations}), restarting...")
            placed_pieces = []
            it = 0

        piece = pieces[n]

        placed_piece: Placement | None = None
        for attempt in range(max_placement_attempts):
            position = random_position_inside_polyhedron(problem.polyhedron)
            quaternion = Quaternion(
                s=random.uniform(0, 1),
                u=Vector3D(
                    x=random.uniform(0, 1),
                    y=random.uniform(0, 1),
                    z=random.uniform(0, 1)
                ).normalize()
            )

            placed_piece = Placement(
                index=piece.index,
                vecteur=position,
                quaternion=quaternion
            )

            faces = placed_piece.transformed_faces(piece)

            if any(
                    not point_inside_polyhedron(vertex, problem.polyhedron)
                    for face in faces for vertex in face.get_vertices()
            ):
                print(
                    f"Piece {piece.index} out of bounds when placed at {position} with rotation {quaternion}"
                )
                continue

            if any(
                    placed_piece.intersects(other, pieces)
                    for other in placed_pieces
            ):
                print(
                    f"Piece {piece.index} intersects with already placed pieces when placed at {position} with rotation {quaternion}"
                )
                continue

            break

        if placed_piece is not None:
            placed_pieces.append(placed_piece)
        else:
            placed_pieces.pop()

    return Solution(
        polyedres=placed_pieces,
        volume=0.0
    )
