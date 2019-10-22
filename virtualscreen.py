import copy
import numpy as np


SCREEN_WIDTH = 2
SCREEN_ASPECT_RATIO = 9 / 16.
SCREEN_HEIGHT = SCREEN_WIDTH * SCREEN_ASPECT_RATIO


class VirtualScreen:
    def __init__(self, observer):
        self._polygons = None
        self._observer = observer

    def start_new_frame(self):
        self._polygons = list()

    def project_object(self, _object):
        projected_object = self._get_projection_on_virtual_screen(_object)
        self._polygons.append(projected_object)

    def get_polygons(self):
        return self._polygons

    def _get_projection_on_virtual_screen(self, _object):
        virtual_object = copy.copy(_object)
        projected_points = [self._get_point_projection(point) for point in _object.vertices]
        virtual_object.vertices = projected_points
        return virtual_object

    def _get_point_projection(self, point):
        screen_center = self._observer.get_screen_center()
        coeff_vec_nom = np.dot(self._observer.direction,
                               screen_center - self._observer.position)
        coeff_vec_denom = np.dot(self._observer.direction,
                                 point - self._observer.position)
        coeff_vec = coeff_vec_nom / float(coeff_vec_denom)
        return self._observer.position + (point - self._observer.position) * coeff_vec
