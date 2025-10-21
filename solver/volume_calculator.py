from typing import Iterable

from solver.types import Point3D, Polyhedron, Vector3D, ProblemDefinition
import numpy as np

def volume_polyhedron_triangles(poly: 'Polyhedron', signed: bool = False) -> float:

    if not poly.vertices or not poly.faces:
        return 0.0

    # conversion de la liste des sommets du polyèdre en un tableau np
    V = np.array([v.to_array() for v in poly.vertices], dtype=np.float64)

    # pareil mais pour les faces + vérification
    F = np.asarray(poly.faces, dtype=int)
    if F.ndim != 2 or F.shape[1] != 3:
        raise ValueError("Toutes les faces doivent être des triangles.")

    if F.min() < 0 or F.max() >= len(V):
        raise IndexError("Indices de face hors bornes des sommets.")

    # Calcule du barycentre et centrage vers 0,0,0
    ref = V.mean(axis=0)
    Vr = V - ref

    # Récupération vectorisée pour a, b, c
    a = Vr[F[:, 0]]
    b = Vr[F[:, 1]]
    c = Vr[F[:, 2]]

    # Produit mixte a . (b * c) / 6, sommation sur toutes les faces
    vol_signed = np.einsum('ij,ij->i', a, np.cross(b, c)).sum() / 6.0

    return float(vol_signed if signed else abs(vol_signed))

def test_calcule_volume(problem: ProblemDefinition)\
        -> float:
    tetra = Polyhedron(
        vertices=[
            Point3D(x=0, y=0, z=0),  # A
            Point3D(x=18, y=0, z=0),  # B
            Point3D(x=0, y=1, z=0),  # C
            Point3D(x=0, y=0, z=1),  # D
        ],
        faces=[
            [0, 2, 1],  # base (A,C,B)
            [0, 1, 3],  # A,B,D
            [0, 3, 2],  # A,D,C
            [1, 2, 3],  # B,C,D
        ],
    )

    print(volume_polyhedron_triangles(tetra))
    print(volume_polyhedron_triangles(problem.polyhedron))

    acc = 0
    for piece in problem.pieces:
        print(piece.vertices)
        print(piece.faces)
        res_volume = volume_polyhedron_triangles(piece)
        print(res_volume)
        acc += res_volume

    print(acc)
    return 0

