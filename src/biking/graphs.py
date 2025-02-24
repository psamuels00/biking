import os

from biking.graph import (
    CaloriesGraph,
    DistanceGraph,
    ElevationGainGraph,
    ElevationLimitsGraph,
    EnergyGraph,
    PerformanceGraph,
    PowerGraph,
    RideRateGraph,
    SpeedGraph,
    TopSpeedGraph,
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
        if self.stats["num_data_tracked_days"] > 0:
            self.generate("power", PowerGraph)
            self.generate("energy", EnergyGraph)
            self.generate("calories", CaloriesGraph)
            self.generate("speed", SpeedGraph)
            self.generate("top_speed", TopSpeedGraph)
            self.generate("elev_gain", ElevationGainGraph)
            self.generate("elev_limits", ElevationLimitsGraph)
            self.generate("performance", PerformanceGraph)
