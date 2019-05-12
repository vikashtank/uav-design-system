# UAV DESIGN SYSTEM

## Notes

This repo is alright, needs improvement, sys.path should not be used to run modules ect. 

## Dependencies
- Python 3
- [Bezier Library](https://github.com/dhermes/bezier)
- [Xfoil v6.97](http://web.mit.edu/drela/Public/web/xfoil/)
- [Athena Vortex Lattice v3.35](http://web.mit.edu/drela/Public/web/avl/)
- macOS

## Capabilities
- Creating aerofoils from bezier curves:
    - infinite number of nodes
    - Vary degree of bezier curve
    - plotting
    - writing Xfoil aerofoil input files
- Automating Xfoil with aerofoil files
    - various angle of attack simulations
    - varying Reynolds number simulations
- Automated Running of Athena Vortex Lattice solver with input files
    - building single wing surfaces
    - Adding flaps and/or elevators
    - running analysis at trim conditions with various outputs:
        - stability derivatives
        - total forces
        - hinge moments
        - force distributions
        - shear and moment distributions
    - varying mesh density and distribution functions as allowed in AVL
    - use of aerofoil files

## Future work
- Writing aerofoil files for SOLIDWORKS input
- Athena Vortex lattice link to Xfoil
- Mesh/Panel inputs for Xfloil
- Aerofoil Blending
- Aerofoil Reshaping
- XFoil flap design
- Viscous Drag Interpolation from XFoil results
- Designing multiple surfaces for use in AVL
- Use of NACA aerofoil inputs to AVL, without the use of input files

## How To Guide

### [Aerofoil](aerofoil)

The [aerofoil](aerofoil) folder contains code to design aerofoils with bezier
curves.

The `Surface` class takes the control nodes of the bezier and two surfaces
are used to create the pressure and suction surfaces of an aerofoil.

The `aerofoil` class takes two surface classes and has the capability of
plotting and writing to a file for Xfoil importing. An additional static method
`develop_aerofoil` provides inputs to design an aerofoil with control points constrained.

`main.py` is a file that runs a simple plotting example

#### Example

```python
import os

import matplotlib.pyplot as plt

from aerofoil import *


# create an aerofoil class from the nodes
aerofoil = Aerofoil.develop_aerofoil(0.1, -0.1, 0.2, 0.5, 0.)

# create a file path to write the coordinates of the aerofoil to
dir_name = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(dir_name, "aerofoil.txt")

# write to coords to file
with open(file_name, "w") as open_file:
    aerofoil.write(open_file)

# plot aerofoil
plot = aerofoil.plot()
plot.axis("equal")
plt.show()
```
