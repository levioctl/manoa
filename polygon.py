import numpy as np


class Polygon:
    def __init__(self, vertex1, vertex2, vertex3, vertex4):
        self.vertices = np.array((vertex1, vertex2, vertex3, vertex4))
        self.color = 'white'

