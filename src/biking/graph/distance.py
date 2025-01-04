from .base import Graph


class DistanceGraph(Graph):
    def build(self, ax1):
        self.title("Distance")

        self.x_axis_days(ax1)
        self.y_axis_distance(ax1)

        self.legend("upper left")