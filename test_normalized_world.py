import unittest
import numpy as np

import observer
import normalized_world


class Test(unittest.TestCase):
    def setUp(self):
        self._observer = observer.Observer()
        self._tested = normalized_world.NormalizedWorld(self._observer)

    def test_screen_center_projection(self):
        screen_center = self._observer.position + self._observer.direction
        self._validate_point_projection(src=screen_center, expected_dst=np.array((0, 0, 0.)))

    def test_one_unit_far_from_screen_center(self):
        point = self._observer.position + 2. * self._observer.direction
        self._validate_point_projection(src=point, expected_dst=np.array((0, 0, 1.)))

    def _validate_point_projection(self, src, expected_dst):
        p = self._tested.project_point(src)

        assert np.isclose(p[0], expected_dst[0]), p
        assert np.isclose(p[1], expected_dst[1]), p
        assert np.isclose(p[2], expected_dst[2]), p


if __name__ == "__main__":
    unittest.main()

