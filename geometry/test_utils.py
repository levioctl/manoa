import unittest
import numpy as np

import line
import plane
import utils


class Test(unittest.TestCase):
    def test_plane_and_line_intersection(self):
        # Setup
        some_point_on_plane = np.array([-2, -4, -4])
        plane_normal = np.array([3, 2, -4])
        _plane = plane.Plane(some_point_on_plane=some_point_on_plane, normal=plane_normal)
        _line = line.Line(point_a=np.array([2, 2, 7]), point_b=np.array([1, 3, 5]))

        # Run
        result = utils.get_plane_and_line_intersection(_plane, _line)

        # Validate
        print(result)
        self.assertTrue(np.isclose(result[0], -0.86, atol=0.1))
        self.assertTrue(np.isclose(result[1], 4.86, atol=0.1))
        self.assertTrue(np.isclose(result[2], 1.29, atol=0.1))


if __name__ == "__main__":
    unittest.main()


