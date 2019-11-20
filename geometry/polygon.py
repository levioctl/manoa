import numpy as np

from geometry import segment


class Polygon:
    def __init__(self, vertex1, vertex2, vertex3, color='white', name="unknown"):
        self.segments = [segment.Segment(vertex1, vertex2, color, name=name + "_1"),
                         segment.Segment(vertex2, vertex3, color, name=name + "_2"),
                         segment.Segment(vertex3, vertex1, color, name=name + "_3"),
                         ]
        self.name = name
        self.color = 'white'
