import numpy as np

import numfor
from rich.progress import track

project_name = "test"
N = 3000
M = 30
dt = 0.000001
N_inter_steps = 200
N_measures = 1701


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
with open("out.dat", "w") as file:
    for i in track(range(N_measures), 'Integration'):
        file.write(f"{time / T} ")
        file.write(" ".join(map(str, x)))
        file.write("\n")
        # Velocity_Verlet_steps(N_inter_steps, gm, F, v, x, num1, num2, N_particles)
        numfor.pefrl_steps(
            steps=N_inter_steps,
            gm=gm,
            v=v,
            x=x,
            num1=num1,
            num2=num2,
            dt=dt,
        )
        time += dt * (N_inter_steps)
