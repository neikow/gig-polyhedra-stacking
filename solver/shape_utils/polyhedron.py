from solver.types import Point3D, Polyhedron, Vector3D


def point_inside_polyhedron(
        point: Point3D,
        polyhedron: Polyhedron,
        epsilon: float = 1e-10,
) -> bool:
    ray_direction = Vector3D(x=1.0, y=0.0, z=0.0)

    intersection_count = 0

    for face_indices in polyhedron.faces:
        if len(face_indices) != 3:
            continue

        p1 = polyhedron.vertices[face_indices[0]]
        p2 = polyhedron.vertices[face_indices[1]]
        p3 = polyhedron.vertices[face_indices[2]]

        intersection = ray_triangle_intersection(point, ray_direction, p1, p2, p3, epsilon)

        if intersection is not None:
            if intersection > epsilon:
                intersection_count += 1

    return intersection_count % 2 == 1


def ray_triangle_intersection(
        ray_origin: Point3D,
        ray_direction: Vector3D,
        p1: Point3D,
        p2: Point3D,
        p3: Point3D,
        epsilon: float,
) -> float | None:
    edge1 = p2 - p1
    edge2 = p3 - p1

    h = ray_direction.cross(edge2)
    a = edge1.dot(h)

    if abs(a) < epsilon:
        return None

    f = 1.0 / a
    s = ray_origin - p1
    u = f * s.dot(h)

    if u < -epsilon or u > 1.0 + epsilon:
        return None

    q = s.cross(edge1)
    v = f * ray_direction.dot(q)

    if v < -epsilon or u + v > 1.0 + epsilon:
        return None

    t = f * edge2.dot(q)

    if t > epsilon:
        return t

    return None