from typing import Union

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel


class Point3D(BaseModel):
    x: float
    y: float
    z: float

    def to_array(self) -> npt.NDArray[np.float64]:
        return np.array([self.x, self.y, self.z])

    def to_vector(self) -> 'Vector3D':
        return Vector3D(x=self.x, y=self.y, z=self.z)

    def __sub__(self, other: Union['Point3D', 'Vector3D']) -> 'Vector3D':
        return Vector3D(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __add__(self, other: Union['Point3D', 'Vector3D']) -> 'Point3D':
        return Point3D(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)


class Vector3D(BaseModel):
    x: float
    y: float
    z: float

    def to_array(self: 'Vector3D') -> npt.NDArray[np.float64]:
        return np.array([self.x, self.y, self.z])

    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __mul__(self, scalar: float) -> 'Vector3D':
        return Vector3D(x=self.x * scalar, y=self.y * scalar, z=self.z * scalar)

    def __rmul__(self, scalar: float) -> 'Vector3D':
        return self.__mul__(scalar)

    def dot(self, other: 'Vector3D') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(
            x=self.y * other.z - self.z * other.y,
            y=self.z * other.x - self.x * other.z,
            z=self.x * other.y - self.y * other.x
        )

    def magnitude(self) -> float:
        return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> 'Vector3D':
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(x=0, y=0, z=0)
        return Vector3D(x=self.x / mag, y=self.y / mag, z=self.z / mag)


class Triangle(BaseModel):
    p1: Point3D
    p2: Point3D
    p3: Point3D

    def get_vertices(self):
        return [self.p1, self.p2, self.p3]


class Polyhedron(BaseModel):
    vertices: list[Point3D]
    faces: list[list[int]]


class Piece(Polyhedron):
    index: int


class ProblemDefinition(BaseModel):
    polyhedron: Polyhedron
    pieces: list[Piece]


class Quaternion(BaseModel):
    s: float
    u: Vector3D


class Placement(BaseModel):
    index: int
    vecteur: Vector3D
    quaternion: Quaternion

    def transformed_faces(self, pieces: Piece) -> list[Triangle]:
        def rotate_point(point: Point3D, quat: Quaternion) -> Point3D:
            u = quat.u
            s = quat.s
            p = point.to_vector()

            term1 = p * (s * s - u.dot(u))
            term2 = u * (2 * u.dot(p))
            term3 = (u.cross(p)) * (2 * s)

            rotated = term1 + term2 + term3
            return Point3D(x=rotated.x, y=rotated.y, z=rotated.z)

        transformed_faces = []
        for face in pieces.faces:
            p1 = pieces.vertices[face[0]]
            p2 = pieces.vertices[face[1]]
            p3 = pieces.vertices[face[2]]

            rp1 = rotate_point(p1, self.quaternion) + self.vecteur
            rp2 = rotate_point(p2, self.quaternion) + self.vecteur
            rp3 = rotate_point(p3, self.quaternion) + self.vecteur

            transformed_faces.append(Triangle(p1=rp1, p2=rp2, p3=rp3))

        return transformed_faces

    def intersects(self, other: 'Placement', pieces: list[Piece]) -> bool:
        from solver.intersection import triangle_intersects_plane

        piece1 = next(piece for piece in pieces if piece.index == self.index)
        piece2 = next(piece for piece in pieces if piece.index == other.index)
        faces1 = self.transformed_faces(piece1)
        faces2 = other.transformed_faces(piece2)

        for face1 in faces1:
            for face2 in faces2:
                if triangle_intersects_plane(face1, face2, epsilon=1e-10):
                    return True
        return False


class Solution(BaseModel):
    volume: float
    polyedres: list[Placement]
