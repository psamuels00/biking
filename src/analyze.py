#!/usr/bin/env python

from biking.input import InputData
from biking.params import Parameters
from biking.graphs import plot_daily_miles
from biking.stats import Statistics


def main():
    parameters = Parameters()
    input_data = InputData()

    statistics = Statistics(input_data)
    statistics.report()

    plot_daily_miles(statistics.stats, parameters.file("mileage"))


main()
