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
        self._visible_zone_bound_planes = self._generate_boundary_walls_planes()

    def start_new_frame(self):
        self._polygons = list()

    def project_object(self, _object):
        _object = self._get_projected_object(_object)
        if _object is not None:
            self._polygons.append(_object)

    def _get_projected_object(self, _object):
        _object = copy.copy(_object)

        if isinstance(_object, segment.Segment):

            _object.vertices = [self._normalized_world.project_point(point) for point in _object.vertices]
            debug = False

            #points_in_front_of_screen = [point for point in _object.vertices if point[2] >= 0]
            points_in_front_of_screen = [point for point in _object.vertices if point[2] >= 0]
            if len(points_in_front_of_screen) == 0:
                pass

            else:
                visible_points = [point for point in _object.vertices if self._is_point_visible(point)]
                if len(visible_points) == 2:
                    stuff = [self._get_point_projection(point) for point in _object.vertices]
                    _object.vertices = stuff
                    return _object
                elif not visible_points and len([point for point in _object.vertices if point[2] < 0]) == 2:
                    if debug:
                        print("no visible points")
                else:
                    #_object.vertices = [self._get_point_projection(point) for point in _object.vertices]
                    #if any(point is None or not point.shape for point in _object.vertices):
                    #    return None
                    #else:
                    #    return _object

                    add_polygon = True
                    non_visible = [point for point in _object.vertices if not [_point for _point in visible_points if _point is point]]
                    assert len(non_visible) in (1, 2)
                    for non_visible_point in non_visible:
                        #visible_point = visible_points[0]
                        other_point = [point for point in _object.vertices if point is not non_visible_point][0]
                        visible_projection = self._get_visible_projection_of_non_visible_point(non_visible_point,
                                                                                               connecting_point=other_point,
                                                                                               debug=debug)

                        if visible_projection is None or "None" in str(visible_projection):
                            add_polygon = False
                            if debug:
                                print("visible projection is none")
                            break
                        else:
                            non_visible_point[0] = visible_projection[0]
                            non_visible_point[1] = visible_projection[1]
                            non_visible_point[2] = visible_projection[2]

                    if add_polygon:
                        _object.vertices = [self._get_point_projection(point) for point in _object.vertices]
                        if any(point is None or not point.shape for point in _object.vertices):
                            if debug:
                                print("not adding polygin, some are none")
                        else:
                            return _object

        elif isinstance(_object, polygon.Polygon):
            _object = copy.copy(_object)
            _object.segments = [self._get_projected_object(_segment)
                                for _segment in _object.segments]
            if all(_segment is not None for _segment in _object.segments):
                return _object

        return None
            #are_some_points_visible = any([self._is_point_visible(point) for point in _object.vertices])
            #if True or are_some_points_visible:
            #    projected_points = [self._get_point_projection(point) for point in _object.vertices]
            #    if projected_points:
            #        _object.vertices = projected_points
            #        self._polygons.append(_object)

    def get_polygons(self):
        return self._polygons

    def _get_point_projection(self, point):
        _plane = plane.Plane(normal=np.array((0, 0, 1)), some_point_on_plane=np.array((0, 0, 0)))
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
        topright = np.array((SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0.))
        topleft = np.array((-SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0.))
        bottomright = np.array((SCREEN_WIDTH / 2., -SCREEN_HEIGHT / 2., 0.))
        bottomleft = np.array((-SCREEN_WIDTH / 2., -SCREEN_HEIGHT / 2., 0.))

        top = plane.create_from_three_points(self._normalized_observer_position, topleft, topright)
        bottom = plane.create_from_three_points(self._normalized_observer_position, bottomleft, bottomright)
        left = plane.create_from_three_points(self._normalized_observer_position, topleft, bottomleft)
        right = plane.create_from_three_points(self._normalized_observer_position, topright, bottomright)
        screen = plane.Plane(normal=np.array((0, 0, 1)), some_point_on_plane=np.array((0, 0, 0)))

        return [top, bottom, left, right, screen]

    def _get_visible_projection_of_non_visible_point(self, invisible_point, connecting_point, debug=False):
        connecting_segment = segment.Segment(invisible_point, connecting_point)

        original_point = np.array(invisible_point)

        min_distance = None
        result = None

        result_idx = None
        for plane_idx, _plane in enumerate(self._visible_zone_bound_planes):
            intersection_point = utils.get_plane_and_segment_intersection(_plane, connecting_segment)
            if intersection_point is not None and "None" not in str(intersection_point):
                #if self._is_point_visible(intersection_point):
                if debug:
                    #import pdb; pdb.set_trace()
                    pass
                condition = False
                if plane_idx == 4:
                    # screen
                    condition = intersection_point[1] >= -SCREEN_HEIGHT / 2. -0.00001 and intersection_point[1] <= SCREEN_HEIGHT / 2 + 0.00001
                else:
                    condition = intersection_point[2] >= -0.001
                if condition:
                    distance_from_inbisible = np.linalg.norm(original_point - intersection_point)
                    if result is None or distance_from_inbisible < min_distance:
                        min_distance = distance_from_inbisible
                        result = intersection_point
                        result_idx = plane_idx

        if debug:
            print("\tline from invisible point {} to connecting point {} intersects with plane {} at point {}".format(invisible_point,
                                                                                                          connecting_point,
                                                                                                          result_idx,
                                                                                                          result))
        return result
