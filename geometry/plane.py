import numpy as np


class Plane:
    def __init__(self, normal, some_point_on_plane):
        self.some_point_on_plane = some_point_on_plane
        self.normal = normal


def create_from_three_points(point_a, point_b, point_c):
    assert not np.array_equal(point_a, point_b)
    assert not np.array_equal(point_a, point_c)

    vec1 = point_a - point_b
    vec2 = point_c - point_b
    normal = np.cross(vec1, vec2)

    return Plane(normal=normal, some_point_on_plane=point_a)

