#!/usr/bin/env python

from biking.graph import (
    DistanceGraph,
    ElevationGainGraph,
    ElevationLimitsGraph,
    PerformanceGraph,
    RideRateGraph,
    SpeedGraph,
    TopSpeedGraph,
)
from biking.input import InputData
from biking.params import Parameters
from biking.stats import Statistics


def calculate_statistics(params, input_data, period):
    statistics = Statistics(params, input_data, period)
    statistics.report()

    return statistics.stats


def generate_graph(params, stats, file_type, type):
    file = params.graph_file(file_type)
    show_only_tracked_days = params.graph.show_only_tracked_days
    linspace_params = params.graph.linspace_params

    graph = type(params, stats, file, show_only_tracked_days, linspace_params)
    graph.generate()


def generate_graphs(params, stats):
    def generate(file_type, type):
        generate_graph(params, stats, file_type, type)

    generate("ride_rate", RideRateGraph)
    generate("distance", DistanceGraph)
    if stats["num_data_tracked_days"] > 0:
        generate("speed", SpeedGraph)
        generate("top_speed", TopSpeedGraph)
        generate("elev_gain", ElevationGainGraph)
        generate("elev_limits", ElevationLimitsGraph)
        generate("performance", PerformanceGraph)


def main():
    params = Parameters()
    input_data = InputData(params)

    for period in ("all", "last30", "last60", "last90"):
        print(period)
        stats = calculate_statistics(params, input_data, period)

        # if stats["num_days"] > 0:
        #     generate_graphs(params, stats)


main()
