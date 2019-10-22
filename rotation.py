import numpy as np


def _get_rotation_matrix(axis_vector, theta):
    l, m, n = axis_vector
    return np.array(((l * l * (1 - np.cos(theta)) + np.cos(theta),
                      m * l * (1 - np.cos(theta)) - n * np.sin(theta),
                      n * l * (1 - np.cos(theta)) + m * np.sin(theta)
                      ),
                     (l * m * (1 - np.cos(theta)) + n * np.sin(theta),
                      m * m * (1 - np.cos(theta)) + np.cos(theta),
                      n * m * (1 - np.cos(theta)) - l * np.sin(theta)
                      ),
                     (l * n * (1 - np.cos(theta)) - m * np.sin(theta),
                      m * n * (1 - np.cos(theta)) + l * np.sin(theta),
                      n * n * (1 - np.cos(theta)) + np.cos(theta)
                      )
                    )
                    )


def rotate(point, axis_vector, theta):
    mat = _get_rotation_matrix(axis_vector, theta)
    return mat.dot(point)
