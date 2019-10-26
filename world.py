import numpy as np

from geometry import segment, polygon


class World:
    def __init__(self):
        self.objects = list()


        #line = segment.Segment(np.array((5., -3., 0.)), np.array((5., 4., 0.)))
        #line.color = 'blue'
        #self.objects.append(line)

        limit = 8.
        for y in range(-int(limit), int(limit)):
            y = float(y)

            if np.abs(y) < 0.001:
                color = 'yellow'
            else:
                color = 'white'

            line = segment.Segment(np.array((-limit, y, 0.)), np.array((limit, y, 0.)), color)
            self.objects.append(line)

            line = segment.Segment(np.array((y, -limit, 0.)), np.array((y, limit, 0.)), color)
            self.objects.append(line)

        self.rec1 = polygon.Polygon(np.array((4., -2., 1.)),
                               np.array((4., -1., 1.)),
                               np.array((4., -1., 0.)),
                               np.array((4., -2., 0.)),
                               color='red')
        self.rec1.color = 'red'
        self.objects.append(self.rec1)

        self.rec2 = polygon.Polygon(np.array((5., -2., 1.)),
                               np.array((5., -1., 1.)),
                               np.array((5., -1., 0.)),
                               np.array((5., -2., 0.)),
                               color='blue')
        self.rec2.color = 'blue'
        self.objects.append(self.rec2)

        self.rec3 = polygon.Polygon(np.array((6., -2., 1.)),
                               np.array((6., -1., 1.)),
                               np.array((6., -1., 0.)),
                               np.array((6., -2., 0.)),
                               color='green')
        self.rec3.color = 'green'
        self.objects.append(self.rec3)

        self.z_axis = segment.Segment(np.array((0., 0., -100.)), np.array((0., 0., 100.)))
        self.objects.append(self.z_axis)

    def update(self):
        return
        self.x_axis.vertices[1][0] -= 10
