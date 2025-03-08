#!/usr/bin/env python

from biking.args import get_program_args
from biking.graphs import Graphs
from biking.html import IndexHtml, InputsDetailsHtml, MetricsDetailsHtml, MetricsSummaryHtml
from biking.input import InputData
from biking.params import Parameters
from biking.stats import Statistics


def generate_everything(params, args):
    periods = (args.period,) if args.period else ("last30", "last60", "last90", "all")
    summary_info = Statistics.init_summary_info()

    for period in periods:
        print(params.report.title[period])

        input_data = InputData(params, period)
        statistics = Statistics(params, period, input_data, summary_info)

        num_days = statistics.stats["num_days"]
        if num_days > 0:
            IndexHtml(params, period).generate_page()
            InputsDetailsHtml(params, period, input_data).generate_page()
            MetricsDetailsHtml(params, period, statistics).generate_page()
            Graphs(params, period, statistics.stats).generate_all()

    if not args.period:
        MetricsSummaryHtml(params, summary_info).generate_page()


def main():
    params = Parameters()
    args = get_program_args()
    period = args.period or "all"

    if args.show_input:
        InputData(params, period).details(args.csv)
    elif args.show_metrics:
        input_data = InputData(params, period)
        Statistics(params, period, input_data).details(args.csv)
    else:
        generate_everything(params, args)


main()
