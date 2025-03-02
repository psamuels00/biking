import os

from biking.graph import (
    CaloriesGraph,
    DistanceGraph,
    ElevationGainGraph,
    ElevationLimitsGraph,
    PerformanceGraph,
    PowerGraph,
    RideRateGraph,
    SpeedGraph,
    TopSpeedGraph,
    WorkGraph,
)


class Graphs:
    def __init__(self, params, period, stats):
        self.params = params
        self.period = period
        self.stats = stats

    def generate(self, file_type, type):
        file = self.params.graph_file(self.period, file_type)

        path = os.path.join(self.params.graph.output_path, self.period)
        os.makedirs(path, exist_ok=True)
        graph = type(self.params, self.stats, file, self.period)
        graph.generate()

    def generate_all(self):
        self.generate("ride_rate", RideRateGraph)
        self.generate("distance", DistanceGraph)
        if self.stats["num_biked_days"] > 0 or self.params.graph.generate_for_no_data:
            self.generate("power", PowerGraph)
            self.generate("work", WorkGraph)
            self.generate("calories", CaloriesGraph)
            self.generate("speed", SpeedGraph)
            self.generate("top_speed", TopSpeedGraph)
            self.generate("elev_gain", ElevationGainGraph)
            self.generate("elev_limits", ElevationLimitsGraph)
            self.generate("performance", PerformanceGraph)
