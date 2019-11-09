import numpy as np
import math

from geometry import rotation


class NormalizedWorld:
    def __init__(self, observer):
        self._observer = observer
        self._current_direction = self._observer.direction
        self._normalize_point_transformation = self._get_virtual_screen_to_normalized_screen_transformation()

    def project_point(self, point):
        self._update_transformation_if_needed()

        point = np.array(point)

        # Bring screen center to origin
        point -= self._observer.get_screen_center()

        #point = self._normalize_point_transformation.dot(point)

        # Rotate around Z axis so that screen's right and left sides are parallel with Y axis
        plane_perpendicular = np.array(self._observer.direction)
        direction_x, direction_y, direction_z = plane_perpendicular
        if direction_x != 0:
            theta = np.pi / 2. - math.atan2(direction_y, direction_x)
            z_axis_unit_vector = [0., 0., 1.]
            rotation_matrix = rotation.get_rotation_matrix(axis_vector=z_axis_unit_vector, theta=theta)
            point = np.dot(rotation_matrix, point)

            # Update plane perpendicular
            plane_perpendicular = rotation.rotate(plane_perpendicular,
                                                  axis_vector=z_axis_unit_vector,
                                                  theta=theta)
            direction_x, direction_y, direction_z = plane_perpendicular

        # Rotate around X axis so that screen is on X-Y plane (and screen's center vertical
        # is on Y axis)
        if direction_y != 0:
            theta = - np.pi / 2. - math.atan2(direction_z, direction_y)
            x_axis_unit_vector = [1., 0., 0.]
            rotation_matrix = rotation.get_rotation_matrix(axis_vector=x_axis_unit_vector, theta=theta)
            point = np.dot(rotation_matrix, point)
            # Update plane perpendicular
            plane_perpendicular = rotation.rotate(plane_perpendicular,
                                                  axis_vector=x_axis_unit_vector,
                                                  theta=theta)
            direction_x, direction_y, direction_z = plane_perpendicular

        ## Rotate around Y axis so that observer is in z==-1
        #if direction_y != 0:
        #    theta = np.pi
        #    y_axis_unit_vector = [0., 1., 0.]
        #    rotation_matrix = rotation.get_rotation_matrix(axis_vector=y_axis_unit_vector, theta=theta)
        #    point = np.dot(rotation_matrix, point)
        #    # Update plane perpendicular
        #    plane_perpendicular = rotation.rotate(plane_perpendicular,
        #                                          axis_vector=y_axis_unit_vector,
        #                                          theta=theta)
        #    direction_x, direction_y, direction_z = plane_perpendicular
        point[2] = -point[2]


        return point

    def _update_transformation_if_needed(self):
        if not np.array_equal(self._observer.direction, self._current_direction):
            self._current_direction = self._observer.direction
            self._normalize_point_transformation = self._get_virtual_screen_to_normalized_screen_transformation()

    def _get_virtual_screen_to_normalized_screen_transformation(self):
        transformation = np.identity(3)

        # Rotate around Z axis so that screen's right and left sides are parallel with Y axis
        plane_perpendicular = np.array(self._observer.direction)
        direction_x, direction_y, direction_z = plane_perpendicular
        if direction_x != 0:
            theta = np.pi / 2. - math.atan2(direction_y, direction_x)
            z_axis_unit_vector = [0., 0., 1.]
            rotation_matrix = rotation.get_rotation_matrix(axis_vector=z_axis_unit_vector, theta=theta)
            transformation = np.matmul(transformation, rotation_matrix)

            # Update plane perpendicular
            plane_perpendicular = rotation.rotate(plane_perpendicular,
                                                  axis_vector=z_axis_unit_vector,
                                                  theta=theta)
            direction_x, direction_y, direction_z = plane_perpendicular

        # Rotate around X axis so that screen is on X-Y plane (and screen's center vertical
        # is on Y axis)
        if direction_y != 0:
            theta = np.pi / 2. - math.atan2(direction_z, direction_y)
            #theta = - math.atan2(direction_z / direction_y)
            x_axis_unit_vector = [1., 0., 0.]
            rotation_matrix = rotation.get_rotation_matrix(axis_vector=x_axis_unit_vector, theta=theta)
            transformation = np.matmul(rotation_matrix, transformation)
            # No need to update plane perpendicular since it's not going to be used anymore
            plane_perpendicular = rotation.rotate(plane_perpendicular,
                                                  axis_vector=x_axis_unit_vector,
                                                  theta=theta)

        return transformation
