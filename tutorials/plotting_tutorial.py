from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/..")  # so uggo thanks to atom runner
import uav_design_system.athena_vortex_lattice as avl
import matplotlib.pyplot as plt


if __name__ == "__main__":

    surface = avl.Surface("UAV")
    surface.define_mesh(20, 30, 1.0, 1.0)

    cord1 = 0.8
    section1 = avl.Section("aerofoil.txt", cord1)

    cord2 = 0.3
    section2 = avl.Section("aerofoil.txt", cord2)
    section2.translation_bias(cord1  - cord2, 0.3, 0)

    cord3 = 0.05
    section3 = avl.Section("aerofoil.txt", cord3)
    section3.translation_bias(cord1 - cord3, 0.85, 0)

    control_surface = avl.ControlSurface("elevator", 0.3, [0, 1, 0], avl.ControlDeflectionType.SYMMETRIC)
    surface.add_section(section1, section2, section3)
    surface.add_control_surface(control_surface, 1, 2)
    surface.reflect_surface = True

    # plotting aircraft
    x, y, z = surface.get_plot_coordinates()

    plt.plot(x, y)
    plt.axes().set_aspect('equal')
    plt.show()
