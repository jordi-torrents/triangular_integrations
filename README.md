
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

<img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/0a3befcf6837a01f7a1586e0834b134c.svg?invert_in_darkmode" align=middle width=98.42109914999997pt height=22.831056599999986pt/> indicate a 2 dimensinal system. Removing them would bring the system to 1D.

<p align="center"><img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/e2bd36f3145a926bd42f3a336c0384a8.svg?invert_in_darkmode" align=middle width=138.74113275pt height=38.96533905pt/></p>

<p align="center"><img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/413bd8fc286d75a3d72c5fbab6a44d5a.svg?invert_in_darkmode" align=middle width=180.738129pt height=38.96533905pt/></p>

<p align="center"><img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/3562e55d8cc02a99026c6bfb49cc00ec.svg?invert_in_darkmode" align=middle width=242.9490822pt height=14.42921535pt/></p>

with
<p align="center"><img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/e1c480f7937c0191a068fb1775cadd34.svg?invert_in_darkmode" align=middle width=356.05290105pt height=99.1177539pt/></p>


Forces can be rewritten as:

<p align="center"><img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/77c227773a3786c6940697543103e48e.svg?invert_in_darkmode" align=middle width=473.03189669999995pt height=184.30546034999998pt/></p>

where

<p align="center"><img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/3f274456baf00443f0b9fa854d3530e4.svg?invert_in_darkmode" align=middle width=392.66359769999997pt height=63.85783634999999pt/></p>

are fixed parameters not depending on <img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=9.39498779999999pt height=14.15524440000002pt/> and, thus, can be computed beforehand.

### Boundary conditions
#### <img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/60931310d3828bd99080883e02a873f4.svg?invert_in_darkmode" align=middle width=35.80006649999999pt height=21.68300969999999pt/>

<p align="center"><img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/d0c737b969091e155022e1f698be4db3.svg?invert_in_darkmode" align=middle width=367.8708198pt height=43.30602705pt/></p>


#### <img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/9ecfc83f78777c2104ce47ad578fcd96.svg?invert_in_darkmode" align=middle width=42.580847099999986pt height=22.465723500000017pt/>

<p align="center"><img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/90fb8de671f1e13896361d311ed63483.svg?invert_in_darkmode" align=middle width=348.29973915pt height=39.301430849999996pt/></p>

To simplify the code, we will set the numerator of the second fraction as a special value in <img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/10c4c2dd540d7169e6aff30edddac385.svg?invert_in_darkmode" align=middle width=23.51834099999999pt height=28.310511900000005pt/>

### Initial conditions

The superindex <img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/3782fad0fede8fa31e7e60df0bfcdb31.svg?invert_in_darkmode" align=middle width=21.175342649999987pt height=27.91243950000002pt/> indicates <img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/5b7d700b9c75a7e9bf83f28d7c9e4ff8.svg?invert_in_darkmode" align=middle width=64.32074384999999pt height=24.65753399999998pt/>

<p align="center"><img src="https://rawgit.com/jordi-torrents/triangular_integrations/None/svgs/2a328edf856b2380790fca906a7d678a.svg?invert_in_darkmode" align=middle width=482.04301200000003pt height=170.96048474999998pt/></p>
