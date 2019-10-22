import numpy as np


class Observer:
    def __init__(self):
        self.direction = np.array((1., 0., 0.))
        self.position = np.array((0., 0., 1.))

    def get_screen_center(self):
        return self.position + self.direction
