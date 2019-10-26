import numpy as np

from geometry import line


def get_plane_and_line_intersection_coeff_vec(_plane, _line):
    coeff_vec_nom = np.dot(_plane.normal, _plane.some_point_on_plane - _line.point_a)
    coeff_vec_denom = np.dot(_plane.normal, _line.point_b - _line.point_a)
    if coeff_vec_denom == 0:
        return None
    coeff_vec = coeff_vec_nom / float(coeff_vec_denom)
    return coeff_vec

def get_plane_and_line_intersection(_plane, _line):
    coeff_vec = get_plane_and_line_intersection_coeff_vec(_plane, _line)
    if coeff_vec is None:
        return None
    return _line.point_a + (_line.point_b - _line.point_a) * coeff_vec


def get_plane_and_segment_intersection(_plane, _segment):
    coeff_vec = get_plane_and_line_intersection_coeff_vec(_plane, line.Line(*_segment.vertices))

    if coeff_vec is None:
        return None

    # Line does not intersect
    if coeff_vec <= 0 or coeff_vec > 1:
        return None

    return _segment.vertices[0] + (_segment.vertices[1] - _segment.vertices[0]) * coeff_vec
