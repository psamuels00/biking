import argparse


def exclusive_show_args(parser):
    group = parser.add_mutually_exclusive_group()

    message = "Show inputs on the console instead of generating graphs."
    group.add_argument("-i", "--show-input", action="store_true", help=message)

    message = "Show metrics on the console instead of generating graphs."
    group.add_argument("-m", "--show-metrics", action="store_true", help=message)


def exclusive_period_args(parser):
    group = parser.add_mutually_exclusive_group()

    message = "Select period for graphs, inputs, and metrics.  The default is 'all' if not specified."
    group.add_argument("-p", "--period", choices=["last30", "last60", "last90", "all"], help=message)

    message = "Shorthand for --period last30"
    group.add_argument("-3", action="store_const", dest="period", const="last30", help=message)

    message = "Shorthand for --period last60"
    group.add_argument("-6", action="store_const", dest="period", const="last60", help=message)

    message = "Shorthand for --period last90"
    group.add_argument("-9", action="store_const", dest="period", const="last90", help=message)

    message = "Shorthand for --period all"
    group.add_argument("-a", action="store_const", dest="period", const="all", help=message)


def get_program_args():
    parser = argparse.ArgumentParser(description="Generate biking performance graphs from data collected using Strava.")

    message = "Format inputs and/or metrics as CSV.  Ignored unless -i or -m option is used."
    parser.add_argument("-c", "--csv", action="store_true", help=message)

    exclusive_show_args(parser)
    exclusive_period_args(parser)

    args = parser.parse_args()

    return args
