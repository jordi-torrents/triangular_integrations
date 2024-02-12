from pathlib import Path

import integrators
import numpy as np
from rich.progress import track


def main(
    N: int, M: int, dt: float, n_measures: int, measure_length: int, output_file: Path
) -> None:
    gm = 1.0
    n_0 = 1.0
    w = 1.0
    Rmu = 1.0
    V_mu = 1.0

    R0 = np.sqrt(2.0) * Rmu
    T = 2.0 * np.pi

    dt = dt * T

    Delta_x = R0 / ((N - M) + 4 / 3)
    delta_t = Delta_x / (3 * V_mu)

    x = np.empty((N + 1))
    num1 = np.empty((N + 1))
    num2 = np.empty((N + 1))

    for i in range(M + 1):
        x[i] = R0 + 2 * V_mu * delta_t - Delta_x * i / M

    for i in range(M + 1, N + 1):
        x[i] = R0 + 2 * V_mu * delta_t - Delta_x * (i - M + 1)

    v = 2 * V_mu + (2 / 3) * (x - (R0 + 2 * V_mu * delta_t)) / delta_t
    v[x < (R0 - V_mu * delta_t)] = 0

    for i in range(1, N + 1):

        x1 = (x[i - 1] + x[i]) / 2
        if x1 < (R0 - V_mu * delta_t):
            num1[i] = (x[i - 1] - x[i]) * 0.5 * (x[i - 1] + x[i])
        else:
            num1[i] = (
                ((x1 - (R0 + 2 * V_mu * delta_t)) / delta_t) ** 2
                * (x[i - 1] - x[i])
                * 0.5
                * (x[i - 1] + x[i])
                / (9 * gm)
            )

    for i in range(N):

        x1 = 0.50 * (x[i + 1] + x[i])
        if x1 <= (R0 - V_mu * delta_t):
            num2[i] = (x[i] - x[i + 1]) * 0.5 * (x[i + 1] + x[i])
        else:
            num2[i] = (
                ((x1 - (R0 + 2 * V_mu * delta_t)) / delta_t) ** 2
                * (x[i] - x[i + 1])
                * 0.5
                * (x[i + 1] + x[i])
                / (9 * gm)
            )

    num2[N] = x[N] * 0.5 * x[N]

    time = delta_t
    with output_file.open("w") as file:
        for i in track(range(n_measures), "Integration"):
            file.write(f"{time / T} ")
            file.write(" ".join(map(str, x)))
            file.write("\n")
            # integrators.velocity_verlet_steps(
            #     steps=measure_length,
            #     v=v,
            #     x=x,
            #     num1=num1,
            #     num2=num2,
            #     dt=dt,
            # )
            integrators.pefrl_steps(
                steps=measure_length,
                v=v,
                x=x,
                num1=num1,
                num2=num2,
                dt=dt,
            )
            time += dt * (measure_length)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-o", dest="output_file", type=Path, required=True)
    parser.add_argument("-N", type=int, default=3000)
    parser.add_argument("-M", type=int, default=30)
    parser.add_argument("-dt", type=float, default=0.000001)
    parser.add_argument("-measure_length", type=int, default=200)
    parser.add_argument("-n_measures", type=int, default=1700)
    args = vars(parser.parse_args())

    for key, value in args.items():
        print(f"  {key}={value}")

    main(**args)
