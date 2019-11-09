import numpy as np


class Observer:
    def __init__(self):
        self.direction = np.array((0.9, 0., -0.5))
        self.position = np.array((-7., 0., 4.5))

    def get_screen_center(self):
        return self.position + self.direction

