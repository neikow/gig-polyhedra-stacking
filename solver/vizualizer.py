import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from solver.types import Solution, ProblemDefinition, Polyhedron, Piece


def draw_container_polyhedron(ax: Axes3D, polyhedron: Polyhedron) -> None:
    verts = [[(polyhedron.vertices[vert_idx].x,
               polyhedron.vertices[vert_idx].y,
               polyhedron.vertices[vert_idx].z) for vert_idx in face] for face in polyhedron.faces]

    ax.add_collection3d(Poly3DCollection(verts, alpha=.25, linewidths=1))


def visualize_solution(problem: ProblemDefinition, solution: Solution) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    draw_container_polyhedron(ax, problem.polyhedron)

    for placement in solution.polyedres:
        piece: Piece = next(p for p in problem.pieces if p.index == placement.index)

        faces = placement.transformed_faces(piece)
        for face in faces:
            verts = [(vertex.x, vertex.y, vertex.z) for vertex in face.get_vertices()]
            poly3d = [[verts[0], verts[1], verts[2]]]
            ax.add_collection3d(
                Poly3DCollection(
                    poly3d, alpha=.5, linewidths=1, edgecolors='b'
                )
            )

    plt.show()
