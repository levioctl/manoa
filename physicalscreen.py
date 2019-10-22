import copy
import numpy as np

import polygon
import rotation
import virtualscreen


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
        # Bring screen center to origin
        point -= self._observer.get_screen_center()

        # Rotate around Z axis so that screen's right and left sides are parallel with Y axis
        plane_perpendicular = np.array(self._observer.direction)
        direction_x, direction_y, direction_z = plane_perpendicular
        if direction_x != 0:
            theta = np.pi / 2 - np.arctan(direction_y / direction_x)
            z_axis_unit_vector = [0, 0, 1]
            point = rotation.rotate(point, axis_vector=z_axis_unit_vector, theta=theta)

            # Update plane perpendicular
            plane_perpendicular = rotation.rotate(plane_perpendicular,
                                                  axis_vector=z_axis_unit_vector,
                                                  theta=theta)
            direction_x, direction_y, direction_z = plane_perpendicular

        # Rotate around X axis so that screen is on X-Y plane (and screen's center vertical
        # is on Y axis)
        if direction_y != 0:
            theta = -(np.pi / 2 - np.arctan(direction_z / direction_y))
            x_axis_unit_vector = [1, 0, 0]
            point = rotation.rotate(point, axis_vector=x_axis_unit_vector, theta=theta)
            # No need to update plane perpendicular since it's not going to be used anymore

        # Move screen to reside only on X>0,Y>0 quarter (since now screen center is at origin)
        point[0] += virtualscreen.SCREEN_WIDTH / 2.
        point[1] += virtualscreen.SCREEN_HEIGHT / 2.
        point[2] = 0

        #try:
        #    assert point[0] <= virtualscreen.SCREEN_WIDTH
        #    assert point[0] >= 0
        #    assert point[1] <= virtualscreen.SCREEN_HEIGHT
        #    assert point[1] >= 0
        #    assert np.isclose(point[2], 0)
        #except:
        #    import pdb; pdb.set_trace()
        #    import sys
        #    sys.exit(1)

        # Scale screen to physical screen size
        #import pdb; pdb.set_trace()
        point[0] *= self._width / virtualscreen.SCREEN_WIDTH
        point[1] *= self._height / virtualscreen.SCREEN_HEIGHT

        #import pdb; pdb.set_trace()
        # Invert Y axis since in the physical screen, Y grows downwards
        point[1] = self._height - point[1]


        return point
