from .base import Graph


class ElevationGraph(Graph):
    def build(self, ax1):
        self.title("Elevation")

        self.x_axis_days(ax1)
        self.y_axis_elevation(ax1)

        self.legend("upper left")