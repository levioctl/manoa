import copy
import numpy as np

import virtualscreen
from geometry import polygon, rotation, segment


class PhysicalScreen:
    def __init__(self, width, height, observer):
        self._width = width
        self._height = height
        self._objects = list()
        self._observer = observer

    def start_new_frame(self):
        self._objects = list()

    def project_virtual_object(self, virtual_object):
        virtual_object = copy.copy(virtual_object)
        physical_object = self._get_physical_object_from_virtual(virtual_object)
        if isinstance(physical_object, list):
            import pdb; pdb.set_trace()
        self._objects.append(physical_object)

    def get_polygons(self):
        return self._objects

    def _get_physical_object_from_virtual(self, virtual_object):
        physical_object = copy.deepcopy(virtual_object)
        if isinstance(virtual_object, segment.Segment):
            physical_object = self._get_physical_segment_from_virtual(virtual_object)
        else:
            physical_object.segments = [self._get_physical_segment_from_virtual(_segment)
                                        for _segment in virtual_object.segments
                                        if _segment is not None]
        return physical_object

    def _get_physical_segment_from_virtual(self, _segment):
        _segment = copy.deepcopy(_segment)
        _segment.vertices = [self._transform_virtual_point_to_physical(np.array(vertex))
                             for vertex in _segment.vertices]
        return _segment

    def _transform_virtual_point_to_physical(self, point):
        # Move screen to reside only on X>0,Y>0 quarter (since now screen center is at origin)
        try:
            point[0] += virtualscreen.SCREEN_WIDTH / 2.
        except:
            import pdb; pdb.set_trace()
        point[1] += virtualscreen.SCREEN_HEIGHT / 2.
        point[2] = 0

        # Scale to physical screen size
        point[0] *= self._width / virtualscreen.SCREEN_WIDTH
        point[1] *= self._height / virtualscreen.SCREEN_HEIGHT

        # Invert Y axis since in the physical screen, Y grows downwards
        point[1] = self._height - point[1]

        return point
