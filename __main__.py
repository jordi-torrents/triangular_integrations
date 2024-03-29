from pathlib import Path

import numpy as np
from rich.progress import track

import integrators


def main(
    N: int,
    M: int,
    dt: float,
    n_measures: int,
    measure_length: int,
    output_file: Path,
    dimensions: int,
) -> None:
    assert dimensions in (1, 2)

    gm = 1.0
    n_0 = 1.0
    w = 1.0
    Rmu = 1.0
    V_mu = 1.0

    R0 = np.sqrt(2.0) * Rmu
    T = 2.0 * np.pi

    dt = dt * T

    Delta_x = R0 / (N - M + 4 / 3)
    delta_t = Delta_x / (3 * V_mu)

    x = np.empty((N + 1))
    phi_minus = np.empty((N + 1))
    phi_plus = np.empty((N + 1))

    x[:] = R0 + 2 * V_mu * delta_t

    for i in range(M + 1):
        x[i] -= Delta_x * i / M

    for i in range(M + 1, N + 1):
        x[i] -= Delta_x * (i - M + 1)

    v = 2 * V_mu + (2 / 3) * (x - (R0 + 2 * V_mu * delta_t)) / delta_t
    v[x < (R0 - V_mu * delta_t)] = 0

    # phi_minus
    for i in range(1, N + 1):
        phi_minus[i] = -2 * gm * (x[i - 1] - x[i])

    if dimensions == 2:
        for i in range(1, N + 1):
            phi_minus[i] *= x[i - 1] + x[i]

    # add the density term
    for i in range(1, N + 1):
        x_ = (x[i - 1] + x[i]) / 2
        if x_ > (R0 - V_mu * delta_t):
            phi_minus[i] *= ((x_ - (R0 + 2 * V_mu * delta_t)) / delta_t) ** 2 / (9 * gm)

    # phi_plus
    for i in range(N):
        phi_plus[i] = +2 * gm * (x[i] - x[i + 1])

    if dimensions == 2:
        for i in range(N):
            phi_plus[i] *= x[i] + x[i + 1]

    # add the density term
    for i in range(N):
        x_ = (x[i + 1] + x[i]) / 2
        if x_ > (R0 - V_mu * delta_t):
            phi_plus[i] *= ((x_ - (R0 + 2 * V_mu * delta_t)) / delta_t) ** 2 / (9 * gm)

    # special value of phi_plus_N, the density term is one here
    phi_plus[N] = +2 * gm * x[N] * (x[N] if dimensions == 2 else 1)

    time = delta_t
    with output_file.open("w") as file:
        for i in track(range(n_measures), "Integration"):
            file.write(f"{time / T:.8e} ")
            np.savetxt(
                file,
                [x],
                fmt="%.8e",
            )
            # integrators.velocity_verlet_steps(
            #     steps=measure_length,
            #     v=v,
            #     x=x,
            #     num1=num1,
            #     num2=num2,
            #     dt=dt,
            #     dimensions = dimensions,
            # )
            integrators.pefrl_steps(
                steps=measure_length,
                v=v,
                x=x,
                phi_minus=phi_minus,
                phi_plus=phi_plus,
                dt=dt,
                dimensions=dimensions,
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
    parser.add_argument("-dimensions", type=int, default=1, choices=(1, 2))
    args = vars(parser.parse_args())

    for key, value in args.items():
        print(f"  {key}={value}")

    main(**args)
