from typing import TypedDict

class Point3D(TypedDict):
    x: float
    y: float
    z: float

class Vector3D(TypedDict):
    x: float
    y: float
    z: float

class Polyhedron(TypedDict):
    vertices: list[Point3D]
    faces: list[list[int]]

class Piece(Polyhedron):
    index: int

class ProblemDefinition(TypedDict):
    polyhedron: Polyhedron
    pieces: list[Piece]

class Quaternion(TypedDict):
    s: float
    u: Vector3D

class Placement(TypedDict):
    index: int
    vecteur: Vector3D
    quaternion: Quaternion

class Solution(TypedDict):
    volume: float
    polyedres: list[Placement]