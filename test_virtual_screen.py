import unittest
import numpy as np

import observer
import virtualscreen


class OneVertexPolygon:
    def __init__(self, vertex):
        self.vertices = [vertex]


class Test(unittest.TestCase):
    def setUp(self):
        _observer = observer.Observer()
        self._tested = virtualscreen.VirtualScreen(_observer)

    def test_projection(self):
        self._tested.start_new_frame()
        _object = OneVertexPolygon(np.array((4, -2, 1)))
        self._tested.project_object(_object)
        polygons = self._tested.get_polygons()
        assert len(polygons) == 1
        p = polygons[0].vertices[0]
        #[assert p == np.array([2, -0.66666667, 0.33333333])
        assert np.isclose(p[0], 2)
        assert np.isclose(np.float(-0.66666667), p[1])
        assert np.isclose(np.float(0.33333333), p[2])


if __name__ == "__main__":
    unittest.main()
