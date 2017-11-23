"""
Script for generating aerofoil files
"""
import bezier
import numpy as np
import matplotlib.pyplot as plt
from typing import List
import os

from aerofoil import Aerofoil


if __name__ == "__main__":


    # create an aerofoil class from the nodes
    aerofoil = Aerofoil.develop_aerofoil(0.1, -0.1, 0.2, 0.5, 0.)

    # create a file path to write the coordinates of the aerofoil to
    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(dir_name, "hey2.txt")

    # write to coords to file
    with open(file_name, "w") as open_file:
        aerofoil.write(open_file)

    # plot aerofoil
    plot = aerofoil.plot()
    plot.axis("equal")
    plt.show()
