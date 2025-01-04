from .base import Graph


class ComboGraph(Graph):
    def build(self, ax1):
        self.title("Combined Metrics")

        self.x_axis_days(ax1)
        self.y_axis_distance(ax1, for_combined_graph=True)
        self.y_axis_ride_rate(ax1, for_combined_graph=True)

        self.legend()