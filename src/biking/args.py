import argparse


def get_program_args():
    parser = argparse.ArgumentParser(description="Generate biking performance graphs from data collected using Strava.")

    message = "Summarize the metrics on the console instead of generating graphs."
    parser.add_argument("-s", "--summarize", action="store_true", help=message)

    message = "Generate only the 30-day graphs."
    parser.add_argument("-3", "--thirty-day", action="store_true", help=message)

    args = parser.parse_args()

    return args