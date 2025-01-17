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


def calculate_statistics(input_data):
    statistics = Statistics(input_data)
    statistics.report()

    return statistics.stats


def generate_graph(parameters, stats, file_type, type):
    file = parameters.file(file_type)
    only_tracked_days = parameters.only_tracked_days
    linspace_params = parameters.linspace_params

    graph = type(stats, file, only_tracked_days, linspace_params)
    graph.generate()


def generate_graphs(parameters, stats):
    def generate(file_type, type):
        generate_graph(parameters, stats, file_type, type)

    generate("ride_rate", RideRateGraph)
    generate("distance", DistanceGraph)
    if stats["num_data_tracked_days"] > 0:
        generate("speed", SpeedGraph)
        generate("top_speed", TopSpeedGraph)
        generate("elev_gain", ElevationGainGraph)
        generate("elev_limits", ElevationLimitsGraph)
        generate("performance", PerformanceGraph)


def main():
    parameters = Parameters()
    input_data = InputData(parameters)
    stats = calculate_statistics(input_data)
    if stats["num_days"] > 0:
        generate_graphs(parameters, stats)


main()
