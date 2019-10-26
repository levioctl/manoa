import numpy as np

from geometry import segment


class Polygon:
    def __init__(self, vertex1, vertex2, vertex3, vertex4, color='white'):
        self.segments = [segment.Segment(vertex1, vertex2, color), segment.Segment(vertex2, vertex3, color),
                         segment.Segment(vertex3, vertex4, color), segment.Segment(vertex4, vertex1, color)]
        self.color = 'white'
