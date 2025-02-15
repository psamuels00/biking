#!/usr/bin/env python

import matplotlib

matplotlib.use("Agg")  # Use a non-interactive backend, prevent icon popping up in Dock on Mac
import matplotlib.pyplot as plt  # noqa: E402
import os  # noqa: E402

from biking.params import Parameters  # noqa: E402


def tex_files(dir):
    return [f[:-4] for f in os.listdir(dir) if f.endswith(".tex")]


def load_file(file):
    with open(file, "r") as fh:
        return fh.read()


def generate_image(latex_code, file):
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.axis("off")

    plt.text(0.5, 0.5, latex_code, fontsize=4)

    plt.savefig(file, dpi=300, bbox_inches="tight", pad_inches=0.1)
    plt.close()


def main():
    params = Parameters()

    source_path = params.formula.source_path
    output_path = params.formula.output_path
    for file in tex_files(source_path):
        latex_code = load_file(f"{source_path}/{file}.tex")
        latex_code = latex_code.replace("\n", "").replace(r"\\", "\n")
        os.makedirs(output_path, exist_ok=True)
        generate_image(latex_code, f"{output_path}/{file}.png")


main()
