from argparse import ArgumentParser
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

parser = ArgumentParser()
parser.add_argument("input_files", nargs="+", type=Path)
args = parser.parse_args()

for filename in args.input_files:
    data = np.loadtxt(filename).T
    time = data[0]
    x = data[1:]

    fig, ax = plt.subplots()

    for particle in range(0, len(x), 50):
        ax.plot(time, x[particle], "k-", lw=0.5)

    ax.set(
        xlabel="time /T",
        ylim=(0, 2),
        ylabel="$x_i$",
    )

    ax.tick_params(which="both", direction="in", top=True, right=True)
    plt.tight_layout()
    print(f"Saving figure at {filename.with_suffix('.png')}")
    fig.savefig(filename.with_suffix(".png"), dpi=300)
