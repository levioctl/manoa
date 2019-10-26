import unittest
import numpy as np

import rotation


X_AXIS_VECTOR = np.array((1, 0, 0))
Y_AXIS_VECTOR = np.array((0, 1, 0))
Z_AXIS_VECTOR = np.array((0, 0, 1))


class Test(unittest.TestCase):
    def test_rotation_around_x_axis(self):
        point = np.array((0, 1, 0))
        point = rotation.rotate(point, axis_vector=X_AXIS_VECTOR, theta=np.pi / 2)
        self._validate_is_close(point, np.array((0, 0, 1)))

    def test_rotation_around_y_axis(self):
        point = np.array((0, 0, 1))
        point = rotation.rotate(point, axis_vector=Y_AXIS_VECTOR, theta=np.pi / 2)
        self._validate_is_close(point, np.array((1, 0, 0)))

    def test_rotation_around_z_axis(self):
        point = np.array((1, 0, 0))
        point = rotation.rotate(point, axis_vector=Z_AXIS_VECTOR, theta=np.pi / 2)
        self._validate_is_close(point, np.array((0, 1, 0)))

    def _validate_is_close(self, vec1, vec2):
        print(vec1, vec2)
        self.assertTrue(np.isclose(vec1[0], vec2[0]))
        self.assertTrue(np.isclose(vec1[1], vec2[1]))
        self.assertTrue(np.isclose(vec1[2], vec2[2]))


if __name__ == "__main__":
    unittest.main()

