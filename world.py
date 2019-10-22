import numpy as np

import segment
import polygon


class World:
    def __init__(self):
        self.objects = list()


        limit = 50.
        for y in range(-int(limit), int(limit)):
            y = float(y)
            line = segment.Segment(np.array((1., y, 0.)), np.array((limit, y, 0.)))
            line.color = 'white'
            self.objects.append(line)

            line = segment.Segment(np.array((y, -3., 0.)), np.array((y, 3., 0.)))
            line.color = 'white'
            self.objects.append(line)

        self.rec1 = polygon.Polygon(np.array((4., -2., 1.)),
                               np.array((4., -1., 1.)),
                               np.array((4., -1., 0.)),
                               np.array((4., -2., 0.)))
        self.rec1.color = 'red'
        self.objects.append(self.rec1)

        self.rec2 = polygon.Polygon(np.array((5., -2., 1.)),
                               np.array((5., -1., 1.)),
                               np.array((5., -1., 0.)),
                               np.array((5., -2., 0.)))
        self.rec2.color = 'blue'
        self.objects.append(self.rec2)

        self.rec3 = polygon.Polygon(np.array((6., -2., 1.)),
                               np.array((6., -1., 1.)),
                               np.array((6., -1., 0.)),
                               np.array((6., -2., 0.)))
        self.rec3.color = 'green'
        self.objects.append(self.rec3)

        self.y_axis = segment.Segment(np.array((0., -100., 0.)), np.array((0., 100., 0.)))
        self.z_axis = segment.Segment(np.array((0., 0., -100.)), np.array((0., 0., 100.)))
        #self.objects.append(self.y_axis)
        #self.objects.append(self.z_axis)

    def update(self):
        return
        self.x_axis.vertices[1][0] -= 10
