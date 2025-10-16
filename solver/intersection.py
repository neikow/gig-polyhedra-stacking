from solver.types import Triangle, Point3D, Vector3D


def triangles_intersect_3d(tri1: Triangle, tri2: Triangle, epsilon: float = 1e-10) -> bool:
    if are_coplanar(tri1, tri2, epsilon):
        return coplanar_triangles_intersect(tri1, tri2, epsilon)

    if not triangle_intersects_plane(tri1, tri2, epsilon):
        return False

    if not triangle_intersects_plane(tri2, tri1, epsilon):
        return False

    seg1 = triangle_plane_intersection_segment(tri1, tri2, epsilon)
    seg2 = triangle_plane_intersection_segment(tri2, tri1, epsilon)

    if seg1 is None or seg2 is None:
        return False

    return segments_overlap_3d(seg1, seg2, epsilon)


def get_plane_equation(tri: Triangle, epsilon: float):
    v1 = tri.p2 - tri.p1
    v2 = tri.p3 - tri.p1
    normal = v1.cross(v2)

    mag = normal.magnitude()
    if mag < epsilon:
        return None, None

    normal = normal.normalize()
    d = -normal.dot(tri.p1.to_vector())

    return normal, d


def signed_distance_to_plane(point: Point3D, normal: Vector3D, d: float) -> float:
    return normal.dot(point.to_vector()) + d


def are_coplanar(tri1: Triangle, tri2: Triangle, epsilon: float) -> bool:
    normal, d = get_plane_equation(tri1, epsilon)
    if normal is None:
        return False

    for vertex in tri2.get_vertices():
        dist = abs(signed_distance_to_plane(vertex, normal, d))
        if dist > epsilon:
            return False

    return True


def triangle_intersects_plane(tri: Triangle, plane_tri: Triangle, epsilon: float) -> bool:
    normal, d = get_plane_equation(plane_tri, epsilon)
    if normal is None:
        return False

    dists = [signed_distance_to_plane(v, normal, d) for v in tri.get_vertices()]

    if all(dist > epsilon for dist in dists) or all(dist < -epsilon for dist in dists):
        return False

    return True


def triangle_plane_intersection_segment(tri: Triangle, plane_tri: Triangle, epsilon: float):
    normal, d = get_plane_equation(plane_tri, epsilon)
    if normal is None:
        return None

    vertices = tri.get_vertices()
    dists = [signed_distance_to_plane(v, normal, d) for v in vertices]

    intersections = []

    for i in range(3):
        j = (i + 1) % 3
        d1, d2 = dists[i], dists[j]

        if d1 * d2 > epsilon:
            continue

        if abs(d1) < epsilon:
            intersections.append(vertices[i])
        elif abs(d2) < epsilon:
            intersections.append(vertices[j])
        else:
            t = d1 / (d1 - d2)
            vec = vertices[j] - vertices[i]
            point = vertices[i] + (vec * t)
            intersections.append(point)

    unique_intersections = []
    for p in intersections:
        is_duplicate = False
        for up in unique_intersections:
            dist = (p - up).magnitude()
            if dist < epsilon:
                is_duplicate = True
                break
        if not is_duplicate:
            unique_intersections.append(p)

    if len(unique_intersections) >= 2:
        return unique_intersections[0], unique_intersections[1]

    return None


def segments_overlap_3d(seg1: tuple, seg2: tuple, epsilon: float) -> bool:
    dir_vec = seg1[1] - seg1[0]
    len1 = dir_vec.magnitude()

    if len1 < epsilon:
        return point_in_segment(seg1[0], seg2, epsilon)

    dir1 = dir_vec.normalize()

    t2_0 = dir1.dot(seg2[0] - seg1[0])
    t2_1 = dir1.dot(seg2[1] - seg1[0])

    min2, max2 = min(t2_0, t2_1), max(t2_0, t2_1)

    return not (max2 < -epsilon or min2 > len1 + epsilon)


def point_in_segment(point: Point3D, segment: tuple, epsilon: float) -> bool:
    d1 = (point - segment[0]).magnitude()
    d2 = (point - segment[1]).magnitude()
    seg_len = (segment[1] - segment[0]).magnitude()

    return abs(d1 + d2 - seg_len) < epsilon


def point_in_triangle(point: Point3D, tri: Triangle, epsilon: float) -> bool:
    v0 = tri.p3 - tri.p1
    v1 = tri.p2 - tri.p1
    v2 = point - tri.p1

    dot00 = v0.dot(v0)
    dot01 = v0.dot(v1)
    dot02 = v0.dot(v2)
    dot11 = v1.dot(v1)
    dot12 = v1.dot(v2)

    denom = dot00 * dot11 - dot01 * dot01
    if abs(denom) < epsilon:
        return False

    inv_denom = 1 / denom
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom

    return (u >= -epsilon) and (v >= -epsilon) and (u + v <= 1 + epsilon)


def coplanar_triangles_intersect(tri1: Triangle, tri2: Triangle, epsilon: float) -> bool:
    for v in tri1.get_vertices():
        if point_in_triangle(v, tri2, epsilon):
            return True

    for v in tri2.get_vertices():
        if point_in_triangle(v, tri1, epsilon):
            return True

    vertices1 = tri1.get_vertices()
    vertices2 = tri2.get_vertices()

    for i in range(3):
        for j in range(3):
            if edges_intersect_2d(
                    vertices1[i], vertices1[(i + 1) % 3],
                    vertices2[j], vertices2[(j + 1) % 3],
                    epsilon,
            ):
                return True

    return False


def edges_intersect_2d(p1: Point3D, p2: Point3D, p3: Point3D, p4: Point3D, epsilon: float) -> bool:
    def sign(a: Point3D, b: Point3D, c: Point3D) -> Vector3D:
        return (b - a).cross(c - a)

    d1 = sign(p3, p4, p1)
    d2 = sign(p3, p4, p2)
    d3 = sign(p1, p2, p3)
    d4 = sign(p1, p2, p4)

    if d1.magnitude() < epsilon and d2.magnitude() < epsilon:
        return point_in_segment(p1, (p3, p4), epsilon) or \
            point_in_segment(p2, (p3, p4), epsilon)

    if d1.dot(d2) < 0 and d3.dot(d4) < 0:
        return True

    return False
