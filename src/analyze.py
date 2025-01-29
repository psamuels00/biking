#!/usr/bin/env python

import os

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
from biking.template import render


def calculate_statistics(params, input_data, frequency, period):
    statistics = Statistics(params, input_data, frequency, period)
    statistics.report()

    return statistics.stats


def generate_graph(params, stats, frequency, period, file_type, type):
    file = params.graph_file(period, file_type)
    show_only_tracked_days = params.graph.show_only_tracked_days
    linspace_params = params.graph.linspace_params

    path = os.path.join(params.graph.output_path, period)
    os.makedirs(path, exist_ok=True)
    graph = type(params, stats, file, period, show_only_tracked_days, linspace_params)
    graph.generate()


def generate_html(params, frequency, period):
    template_path = params.html.template_path
    template_file = params.html.template_file
    output_path = os.path.join(params.html.output_path, frequency)
    output_file = f"{period}.html"
    data = dict(period=period, frequency=frequency)
    render(template_path, template_file, data, output_path, output_file)

def generate_graphs(params, stats, frequency, period):
    def generate(file_type, type):
        generate_graph(params, stats, frequency, period, file_type, type)

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

    for frequency in ("daily", "weekly", "monthly", "quarterly"):
        for period in ("last30", "last60", "last90", "all"):
            #print(f"{frequency}: {params.report.title[period]}")
            print(frequency, period)
            stats = calculate_statistics(params, input_data, frequency, period)

            if stats["num_days"] > 0:
                generate_html(params, frequency, period)
                generate_graphs(params, stats, frequency, period)


main()
