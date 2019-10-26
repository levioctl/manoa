import copy
import numpy as np

import normalized_world
from geometry import utils, segment, plane, line, segment, polygon


SCREEN_WIDTH = 1
SCREEN_ASPECT_RATIO = 9 / 16.
SCREEN_HEIGHT = SCREEN_WIDTH * SCREEN_ASPECT_RATIO


class VirtualScreen:
    def __init__(self, observer):
        self._polygons = None
        self._normalized_world = normalized_world.NormalizedWorld(observer)
        self._normalized_observer_position = self._normalized_world.project_point(observer.position)
        self._normalized_observer_direction = self._normalized_world.project_point(observer.position)
        self._visible_zone_bound_planes = self._generate_boundary_walls_planes()

    def start_new_frame(self):
        self._polygons = list()

    def project_object(self, _object):
        _object = copy.copy(_object)

        if isinstance(_object, segment.Segment):
            _object.vertices = [self._normalized_world.project_point(point) for point in _object.vertices]


            visible_points = [point for point in _object.vertices if point[2] >= 0]
            if len(visible_points) == 0:
                pass

            else:
                if len(visible_points) == 2:
                    _object.vertices = [self._get_point_projection(point) for point in _object.vertices]
                    self._polygons.append(_object)
                if len(visible_points) == 1:
                    visible_point = visible_points[0]
                    non_visible_point = [point for point in _object.vertices if point is not visible_point][0]
                    visible_projection = self._get_visible_projection_of_non_visible_point(non_visible_point,
                                                                                        connecting_visible_point=visible_point)

                    if visible_projection is not None:
                        non_visible_point[0] = visible_projection[0]
                        non_visible_point[1] = visible_projection[1]
                        non_visible_point[2] = visible_projection[2]

                        _object.vertices = [self._get_point_projection(point) for point in _object.vertices]
                        self._polygons.append(_object)

        elif isinstance(_object, polygon.Polygon):
            for _segment in _object.segments:
                self.project_object(_segment)
            #are_some_points_visible = any([self._is_point_visible(point) for point in _object.vertices])
            #if True or are_some_points_visible:
            #    projected_points = [self._get_point_projection(point) for point in _object.vertices]
            #    if projected_points:
            #        _object.vertices = projected_points
            #        self._polygons.append(_object)

    def get_polygons(self):
        return self._polygons

    def _get_point_projection(self, point):
        screen_center = self._normalized_observer_position + self._normalized_observer_direction
        _plane = plane.Plane(normal=self._normalized_observer_direction,
                             some_point_on_plane=screen_center)
        _line = line.Line(point_a=point, point_b=self._normalized_observer_position)
        return utils.get_plane_and_line_intersection(_plane, _line)

    def _is_point_on_screen_plane_inside_screen(self, point_on_screen_plane):
        return (point_on_screen_plane[0] >= -SCREEN_WIDTH / 2. and point_on_screen_plane[0] <= SCREEN_WIDTH / 2.
                and point_on_screen_plane[1] >= -SCREEN_HEIGHT / 2. and point_on_screen_plane[1] <= SCREEN_HEIGHT / 2.)

    def _is_point_visible(self, point):
        result = False
        if point[2] >= 0:
            point_projection = self._get_point_projection(point)
            if self._is_point_on_screen_plane_inside_screen(point_projection):
                result = True
        return result

    def _generate_boundary_walls_planes(self):
        # Create screen bound points
        topright = np.array((SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0))
        topleft = np.array((-SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0))
        bottomright = np.array((SCREEN_WIDTH / 2., -SCREEN_HEIGHT / 2., 0))
        bottomleft = np.array((-SCREEN_WIDTH / 2., -SCREEN_HEIGHT / 2., 0))

        top = plane.create_from_three_points(self._normalized_observer_position, topleft, topright)
        bottom = plane.create_from_three_points(self._normalized_observer_position, bottomleft, bottomright)
        left = plane.create_from_three_points(self._normalized_observer_position, topleft, bottomleft)
        right = plane.create_from_three_points(self._normalized_observer_position, topright, bottomright)

        return [top, bottom, left, right]

    def _get_visible_projection_of_non_visible_point(self, non_visible_point, connecting_visible_point):
        connecting_segment = segment.Segment(non_visible_point, connecting_visible_point)

        for _plane in self._visible_zone_bound_planes:
            intersection_point = utils.get_plane_and_segment_intersection(_plane, connecting_segment)
            if intersection_point is not None:
                return intersection_point

        return None
