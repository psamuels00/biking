#!/usr/bin/env python

from biking.input import InputData
from biking.params import Parameters
from biking.graph.mileage import MileageGraph
from biking.stats import Statistics


def main():
    parameters = Parameters()
    input_data = InputData()

    statistics = Statistics(input_data)
    statistics.report()

    graph = MileageGraph(statistics.stats, parameters.file("mileage"))
    graph.generate()


main()
