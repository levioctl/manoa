class Segment:
    def __init__(self, point_a, point_b, color="yellow", name="unknown"):
        self.vertices = (point_a, point_b)
        self.color = color
        self.name = name
