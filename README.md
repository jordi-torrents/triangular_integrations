
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
