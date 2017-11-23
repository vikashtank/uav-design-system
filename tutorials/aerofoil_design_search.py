"""
file demonstrating how an aerofoil is created and is run through xfoil to generate
the best values of drag and moment
"""
from os.path import join, exists, dirname, abspath
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/..")  # so uggo thanks to atom runner
import uav_design_system.xfoil as xfoil
import uav_design_system.aerofoil as aerofoil
import matplotlib.pyplot as plt

def run_aerofoil(t_x, t_y, thick, camb_x, camb_y, plot, colour):
    # create an aerofoil class from the nodes
    aero_geom = aerofoil.Aerofoil.develop_aerofoil(t_x, t_y, thick, camb_x, camb_y)

    # create a file path to write the coordinates of the aerofoil to
    dir_name = dirname(abspath(__file__))
    file_name = join(dir_name, "aerofoil.txt")

    # write to coords to file
    with open(file_name, "w") as open_file:
        aero_geom.write(open_file)

    file_path = "/Applications/Xfoil.app/Contents/Resources/xfoil"

    xfoil_runner = xfoil.XfoilRunner(file_path)
    xfoil_runner.setup_analysis(file_name, 1e6)
    results = xfoil_runner.generate_results(0, 5, 0.5, False)

    aero_geom.plot(plot = plot, colour = colour)

    return results["xfoil"]["analysis"]["results"]

if __name__ == "__main__":

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.axis("equal")

    camber = [0, 0.1, 0.2, 0.3]
    colour = ["r", "g", "b", "y"]
    cm = []
    cd = []
    cl = []

    for i in [0, 1, 2, 3]:
        results = run_aerofoil(0.1, -0.1, 0.2, 0.5, camber[i], ax, colour[i])
        cm.append(results[0]["cm"])
        cd.append(results[0]["cd"])
        cl.append(results[0]["cl"])

    fig = plt.figure(2)
    ax = fig.add_subplot(111)
    ax.axis("equal")
    plt.xlabel("cm")
    plt.ylabel("cd")
    plt.plot(cm, cd)

    fig = plt.figure(3)
    ax = fig.add_subplot(111)
    ax.axis("equal")
    plt.xlabel("camber")
    plt.ylabel("moment coefficient")
    plt.plot(camber, cm)

    print(cm)
    print(cd)
    print(cl)

    plt.show()
