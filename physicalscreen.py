import copy
import numpy as np

import virtualscreen
from geometry import polygon, rotation


class PhysicalScreen:
    def __init__(self, width, height, observer):
        self._width = width
        self._height = height
        self._objects = list()
        self._observer = observer

    def start_new_frame(self):
        self._objects = list()

    def project_virtual_object(self, virtual_object):
        physical_object = copy.copy(virtual_object)
        physical_object = self._transform_virtual_polygon_to_physical(physical_object)
        self._objects.append(physical_object)

    def get_polygons(self):
        return self._objects

    def _transform_virtual_polygon_to_physical(self, virtual_object):
        physical_object = copy.deepcopy(virtual_object)
        physical_object.vertices = [self._transform_virtual_point_to_physical(np.array(vertex))
                                    for vertex in virtual_object.vertices]
        return physical_object

    def _transform_virtual_point_to_physical(self, point):
        # Move screen to reside only on X>0,Y>0 quarter (since now screen center is at origin)
        point[0] += virtualscreen.SCREEN_WIDTH / 2.
        point[1] += virtualscreen.SCREEN_HEIGHT / 2.
        point[2] = 0

        # Scale to physical screen size
        point[0] *= self._width / virtualscreen.SCREEN_WIDTH
        point[1] *= self._height / virtualscreen.SCREEN_HEIGHT

        # Invert Y axis since in the physical screen, Y grows downwards
        point[1] = self._height - point[1]


        return point
