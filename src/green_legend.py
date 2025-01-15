#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import os

from biking.params import Parameters


days_of_week = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
text_color = ("black", "black", "black", "black", "white", "white", "white")


def write_file(dir, file, content):
    if not os.path.isdir(dir):
        os.makedirs(dir)

    with open(f"{dir}/{file}", "w") as fh:
        fh.writelines(content)


def html_content(shades_of_green):
    content = ['<div style="display: flex; gap: 2px; font-family: sans-serif;">\n']

    for shade, day, color in zip(shades_of_green, days_of_week, text_color):
        shade = [str(int(n * 255)) for n in shade[:3]]
        bgcolor = "rgb(" + ", ".join(shade) + ")"
        style = (
            f"width: 100px; height: 30px; color: {color}; background-color: {bgcolor};"
            "display: flex; align-items: center; justify-content: center"
        )
        content += [f'    <div style="{style}">{day}</div>\n']

    content += ["</div>\n"]

    return content


def main():
    parameters = Parameters()

    linspace_params = parameters.linspace_params
    shades_of_green = plt.cm.Greens(np.linspace(*linspace_params, 7))
    content = html_content(shades_of_green)

    dir = parameters.green_legend_dir
    file = parameters.green_legend_html_file
    write_file(dir, file, content)


main()