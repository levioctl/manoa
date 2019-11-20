import numpy as np

from geometry import segment, polygon


class World:
    def __init__(self):
        self.objects = list()


        if True:
            #line = segment.Segment(np.array((5., -3., 0.)), np.array((5., 4., 0.)))
            #line.color = 'blue'
            #self.objects.append(line)

            limit = 10
            #nr_lines = 5
            for line_nr in range(-10, 11, 1):

                line = segment.Segment(np.array((-limit, line_nr, 0.)), np.array((limit, line_nr, 0.)), color='white', name="gridy_{}".format(line_nr))
                self.objects.append(line)

                line = segment.Segment(np.array((line_nr, -limit, 0.)), np.array((line_nr, limit, 0.)), color='yellow')
                self.objects.append(line)

        self.tri1 = polygon.Polygon(np.array((4., -2., 1.)),
                               np.array((4., -1., 0.)),
                               np.array((4., -2., 0.)),
                               color='red',
                               name='redsq')
        self.tri1.color = 'red'

        self.tri2 = polygon.Polygon(np.array((5., -2., 1.)),
                               np.array((5., -1., 0.)),
                               np.array((5., -2., 0.)),
                               color='blue')
        self.tri2.color = 'blue'

        self.tri3 = polygon.Polygon(np.array((6., -2., 1.)),
                               np.array((6., -1., 0.)),
                               np.array((6., -2., 0.)),
                               color='green')
        self.tri3.color = 'green'
        self.objects.append(self.tri3)
        self.objects.append(self.tri2)
        self.objects.append(self.tri1)

        squares = [#polygon.Polygon(np.array((-1., -1., 0.)),
                   #                np.array((-1., 1., 0.)),
                   #                np.array((1., 1., 0.)),
                   #                np.array((1., -1., 0.)),
                   #                color='green'),
                   #polygon.Polygon(np.array((-1., -1., 1.)),
                   #                np.array((-1., 1., 1.)),
                   #                np.array((1., 1., 1.)),
                   #                np.array((1., -1., 1.)),
                   #                color='green'),
                   segment.Segment(np.array((-1., -1., +1.)),
                                   np.array((-1., -1., 0.)),
                                   color="green"),
                   segment.Segment(np.array((-1., +1., 1.)),
                                   np.array((-1., +1., 0.)),
                                   color="green"),
                   segment.Segment(np.array((+1., -1., +1.)),
                                   np.array((+1., -1., 0.)),
                                   color="green"),
                   segment.Segment(np.array((+1., +1., +1.)),
                                   np.array((+1., +1., 0.)),
                                   color="green")
                   ]
        for square in squares:
            self.objects.append(square)

        self.x_axis = segment.Segment(np.array((-100., 0., -0.)), np.array((100., 0., 0.)), name="x_axis")

    def update(self):
        return
        self.x_axis.vertices[1][0] -= 10
