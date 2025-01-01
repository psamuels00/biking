#!/usr/bin/env python

from biking.graph import DistanceGraph, ElevationGraph, SpeedGraph
from biking.input import InputData
from biking.params import Parameters
from biking.stats import Statistics


def calculate_statistics(input_data):
    statistics = Statistics(input_data)
    statistics.report()

    return statistics.stats


def generate_graphs(stats):
    parameters = Parameters()
    file = parameters.file

    DistanceGraph(stats, file("distance")).generate()
    ElevationGraph(stats, file("elevation")).generate()
    SpeedGraph(stats, file("speed")).generate()


def main():
    input_data = InputData()
    stats = calculate_statistics(input_data)
    generate_graphs(stats)


main()
