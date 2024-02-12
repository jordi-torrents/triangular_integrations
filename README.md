
# Usage

## 1 Install a Fortran compiler if you don't have one:

Check [how](https://fortran-lang.org/learn/os_setup/install_gfortran/), in Ubuntu:
``` bash
sudo apt install gfortran
```

## 2 Create an environment with Python and Numpy.

Conda environments work great but, actually, you can run this code almost anywhere, there are no strict requirements.

## 3 Compile Fortran subroutines with [Numpy's Fortran to Python](https://numpy.org/doc/stable/f2py/)
``` bash
python -m numpy.f2py -c integrators.f90 -m integrators
```
## 4 Use the library

``` python
import integrators
integrators.pefrl_steps()
```

### `integrators.pefrl_steps(steps:int,v:np.ndarray, x:np.ndarray, num1:np.ndarray, num2:np.ndarray, dt:float)`

You can also use the example code in `__main__.py`. To run it, install first [Rich](https://rich.readthedocs.io/) with `pip install rich`.

# Equations

    (from “Triangular” ideas. Idea 03, “The disk”. Version 010.3)

${\color{red}\text{Red terms}}$ indicate a 2 dimensinal system. Removing them would bring the system to 1D.

$$\ddot{x}_0 =-\frac{g}{m}\frac{-n_{1/2}}{x_{0}-x_{1/2}}\\
\ddot{x}_i =-\frac{g}{m}\frac{n_{i-1/2}-n_{i+1/2}}{x_{i-1/2}-x_{i+1/2}}\\
0<x_N<x_{N-1}<...<x_1<x_0< \infin $$

with
$$\begin{split}
x_{i-1/2} & \equiv \frac{x_{i-1}+x_i}{2} \quad\text{for}\quad 0<i \\
x_{i+1/2} & \equiv \frac{x_i+x_{i+1}}{2} \quad\text{for}\quad i<N \\
x_{N+1/2} & \equiv \frac{x_N}{2} \\

n_{i-1/2} & \equiv n^{\delta t}\left(x^{\delta t}_{i-1/2}\right)\red{\frac{x^{\delta t}_{i-1/2}}{x_{i-1/2}}}\frac{x^{\delta t}_{i-1}-x^{\delta t}_i}{x_{i-1}-x_i}\\
n_{i+1/2} & \equiv n^{\delta t}\left(x^{\delta t}_{i+1/2}\right)\red{\frac{x^{\delta t}_{i+1/2}}{x_{i+1/2}}}\frac{x^{\delta t}_i-x^{\delta t}_{i+1}}{x_i-x_{i+1}}\quad\text{for}\quad i<N \\
n_{N+1/2} & \equiv n^{\delta t}\left(x^{\delta t}_{N+1/2}\right)\red{\frac{x^{\delta t}_{N+1/2}}{x_{N+1/2}}}\frac{x^{\delta t}_N}{x_N} \end{split}$$


Forces can be rewritten as:

$$
\begin{align}

\ddot{x}_i & =-\frac{g}{m}\frac{n_{i-1/2}-n_{i+1/2}}{x_{i-1/2}-x_{i+1/2}}\\

& = -\frac{g}{m}
\frac{
    n^{\delta t}\left(x^{\delta t}_{i-1/2}\right)\red{\frac{x^{\delta t}_{i-1/2}}{x_{i-1/2}}}\frac{x^{\delta t}_{i-1}-x^{\delta t}_i}{x_{i-1}-x_i}
    -n^{\delta t}\left(x^{\delta t}_{i+1/2}\right)\red{\frac{x^{\delta t}_{i+1/2}}{x_{i+1/2}}}\frac{x^{\delta t}_i-x^{\delta t}_{i+1}}{x_i-x_{i+1}}}
{x_{i-1/2}-x_{i+1/2}}\\

& = -2\frac{g}{m}
\frac{
    n^{\delta t}\left(\frac{x^{\delta t}_{i-1}+x^{\delta t}_i}{2}\right)\red{\frac{x^{\delta t}_{i-1}+x^{\delta t}_i}{x_{i-1}+x_i}}\frac{x^{\delta t}_{i-1}-x^{\delta t}_i}{x_{i-1}-x_i}
    -n^{\delta t}\left(\frac{x^{\delta t}_{i+1}+x^{\delta t}_i}{2}\right)\red{\frac{x^{\delta t}_{i}+x^{\delta t}_{i+1}}{x_{i}+x_{i+1}}}\frac{x^{\delta t}_i-x^{\delta t}_{i+1}}{x_i-x_{i+1}}}{x_{i-1}-x_{i+1}}\\

& = \frac{\Phi_i^-}{\red{\left(x_{i-1}+x_i\right)}\left(x_{i-1}-x_i\right)\left(x_{i-1}-x_{i+1}\right)}
   +\frac{\Phi_i^+}{\red{\left(x_i+x_{i+1}\right)}\left(x_i-x_{i+1}\right)\left(x_{i-1}-x_{i+1}\right)}

\end{align}
$$

where

$$
\begin{align}

\Phi_i^-&= -2\frac{g}{m}n^{\delta t}\left(\frac{x^{\delta t}_{i-1}+x^{\delta t}_i}{2}\right)
\red{\left(x^{\delta t}_{i-1}+x^{\delta t}_i\right)}\left(x^{\delta t}_{i-1}-x^{\delta t}_i\right) \\
\Phi_i^+&=+2\frac{g}{m}n^{\delta t}\left(\frac{x^{\delta t}_{i+1}+x^{\delta t}_i}{2}\right)\red{\left(x^{\delta t}_{i}+x^{\delta t}_{i+1}\right)}\left(x^{\delta t}_{i}-x^{\delta t}_{i+1}\right)

\end{align}
$$

are fixed parameters not depending on $x$ and, thus, can be computed beforehand.

### Boundary conditions
#### $i=0$

$$
\begin{align}
\ddot{x}_0 &=-\frac{g}{m}\frac{-n_{1/2}}{x_{0}-x_{1/2}}\\
&=-\frac{g}{m}\frac{-n^{\delta t}\left(x^{\delta t}_{1/2}\right)\red{\frac{x^{\delta t}_{1/2}}{x_{1/2}}}\frac{x^{\delta t}_0-x^{\delta t}_{1}}{x_0-x_{1}}}{x_0-x_{1/2}}\\

&=2\frac{g}{m}\frac{n^{\delta t}\left(\frac{x^{\delta t}_0+x^{\delta t}_1}{2}\right)\red{\frac{x^{\delta t}_0+x^{\delta t}_1}{x_0+x_1}}\frac{x^{\delta t}_0-x^{\delta t}_{1}}{x_0-x_{1}}}{x_0-x_1}\\
&=\frac{\Phi^+_0}{\red{(x_0+x_1)}(x_0-x_1)(x_0-x_1)}
\end{align}
$$


#### $i=N$

$$
\begin{align}
\ddot{x}_N &=-\frac{g}{m}\frac{n_{N-1/2}-n_{N+1/2}}{x_{N-1/2}-x_{N+1/2}}\\
&= -\frac{g}{m}
\frac{
    n^{\delta t}\left(x^{\delta t}_{N-1/2}\right)\red{\frac{x^{\delta t}_{N-1/2}}{x_{N-1/2}}}\frac{x^{\delta t}_{N-1}-x^{\delta t}_N}{x_{N-1}-x_N}
    -n^{\delta t}\left(x^{\delta t}_{N+1/2}\right)\red{\frac{x^{\delta t}_{N+1/2}}{x_{N+1/2}}}\frac{x^{\delta t}_N}{x_N}}
{x_{N-1/2}-x_{N+1/2}}\\
&= -2\frac{g}{m}
\frac{
    n^{\delta t}\left(\frac{x^{\delta t}_{N-1}+x^{\delta t}_N}{2}\right)\red{\frac{x^{\delta t}_{N-1}+x^{\delta t}_N}{x_{N-1}+x_N}}\frac{x^{\delta t}_{N-1}-x^{\delta t}_N}{x_{N-1}-x_N}
    -n^{\delta t}\left(x^{\delta t}_N/2\right)\red{\frac{x^{\delta t}_N}{x_N}}\frac{x^{\delta t}_N}{x_N}}
{x_{N-1}}\\

&= \frac{\Phi^-_N}{\red{(x_{N-1}+x_N)}(x_{N-1}-x_N)x_{N-1}}+\frac{2\frac{g}{m}n^{\delta t}\left(x^{\delta t}_N/2\right)\red{x^{\delta t}_N}x^{\delta t}_N}{\red{x_N}x_Nx_{N-1}}
\end{align}
$$

To simplify the code, we will set the numerator of the second fraction as a special value in $\Phi^+_N$

### Initial conditions

The superindex $f^{\delta t}$ indicates $f(t=\delta t)$

$$
x_i^{\delta t}=
  \Delta x\frac{i}{M}
  \Delta x\left(i-M+1\right)
$$

$$
x_i^{\delta t}=
\begin{cases}
  \Delta x\frac{i}{M} & \text{for}\quad 0\leq i\leq M \\
  \Delta x\left(i-M+1\right) &  \text{for}\quad M\leq i\leq N
\end{cases}

\\

n^{\delta t}(x)=
\begin{cases}
  \frac{1}{9}\frac{m}{g}\left[\frac{x-(R_0+2V_\mu\delta t)}{\delta t}\right]^2 & \text{for}\quad R_0-V_\mu\delta t\leq x\leq R_0+2V_\mu\delta t \\
  n(0) &  \text{for}\quad 0< x\leq R_0-V_\mu\delta t
\end{cases}

\\

\dot{x}^{\delta t}(x)=
\begin{cases}
  2V_\mu+\frac{2}{3}\frac{x-(R_0+2V_\mu\delta t)}{\delta t} & \text{for}\quad R_0-V_\mu\delta t\leq x\leq R_0+2V_\mu\delta t \\
  0 &  \text{for}\quad 0< x\leq R_0-V_\mu\delta t
\end{cases}
$$
