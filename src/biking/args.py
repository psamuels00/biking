import argparse


def get_program_args():
    parser = argparse.ArgumentParser(description="Generate biking performance graphs from data collected using Strava.")

    message = "Generate only the 30-day graphs."
    parser.add_argument("-3", "--thirty-day", action="store_true", help=message)

    message = "Format inputs and/or metrics as CSV.  Ignored unless -i or -m option is used."
    parser.add_argument("-c", "--csv", action="store_true", help=message)

    message = "Show inputs on the console instead of generating graphs."
    parser.add_argument("-i", "--show-input", action="store_true", help=message)

    message = "Show metrics on the console instead of generating graphs.  [Work In Progress]"
    parser.add_argument("-m", "--show-metrics", action="store_true", help=message)

    args = parser.parse_args()

    return args
