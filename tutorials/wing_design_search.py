from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/..")  # so uggo thanks to atom runner
import uav_design_system.athena_vortex_lattice as avl
import shutil

def create_wing(file_name):

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

    with open(file_name, "w") as open_file:
        open_file.write(str(surface))

    return surface


def run_analysis(geom_file, mass_file, config_file, results_dir):

    makedirs(results_dir)

    avl_runner = avl.AVLRunner()
    avl_runner.setup_analysis( geom_file, mass_file, config_file)
    results_dict = avl_runner.generate_results(results_dir)

    return results_dict


if __name__ == "__main__":

    results_dir = "/Users/VikashTank/Desktop/athena_results"
    makedirs(results_dir)

    pho = 1.225
    vel = 30
    g = 9.81
    m = 6.8
    w = m*g

    # create
    avl_file_name = join(results_dir, "test.avl")
    wing = create_wing(avl_file_name)


    surface_area = wing.area
    cl_trim = w/(0.5*vel*vel*pho*surface_area)

    # create run file
    run_file_name = join(results_dir, "test.run")
    print(run_file_name)
    with open( run_file_name, "w") as open_file:
        open_file.write(avl.create_run_file(6.8, 30, 0.5, cl_trim))

    #create dummy mass file
    mass_file_name = join(results_dir, "mass.mass")
    with open( mass_file_name, "w") as open_file:
        open_file.write("")
