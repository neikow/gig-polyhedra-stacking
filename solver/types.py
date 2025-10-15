from pydantic import BaseModel

class Point3D(BaseModel):
    x: float
    y: float
    z: float

class Vector3D(BaseModel):
    x: float
    y: float
    z: float

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

class Solution(BaseModel):
    volume: float
    polyedres: list[Placement]