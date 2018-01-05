"""
Integration test to ensure that AVL accepts the case, plane and mass files
created
"""
from os.path import join, exists, dirname, abspath
from os import makedirs
from shutil import rmtree
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system import layout, athena_vortex_lattice as avl


class Test(unittest.TestCase):

    def setUp(self):
        # make temporary folder
        self.test_folder = join(this_directory, "test_folder")
        makedirs(self.test_folder)

        self.results_dir = join(this_directory, "results")
        makedirs(self.results_dir)

        # create temporary file names
        self.wing_file = join(self.test_folder, "wing.avl")
        self.mass_file = join(self.test_folder, "mass.mass")
        self.run_file = join(self.test_folder, "wing.run")

    def tearDown(self):
        rmtree(self.results_dir)
        rmtree(self.test_folder)

    def test_integration(self):

        # create a surface file ------------------------------------------------
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

        with open(self.wing_file, "w") as open_file:
            open_file.write(surface.to_avl_string())

        # create a mass file ---------------------------------------------------
        # create sustructure from wing
        structure_creator  = layout.StructureFactory(layout.StructuralModelType.HOLLOWFOAM)
        structural_model = structure_creator(surface, wall_thickness = 1)

        # add some more weights and arrangement
        mass_object = layout.MassObject(layout.Cuboid(1, 1, 1), 1)
        mass_object.location = layout.Point(-0.5, -0.5, -0.5)

        arrangement = layout.Arrangement("plane arrangement", mass_object, structural_model, structural_model)

        # create case file -----------------------------------------------------
        case = avl.TrimCase(surface.area * 2, velocity = 22,
                            mass = arrangement.total_mass)
        case.to_file(self.run_file)
        layout.create_mass_file(self.mass_file, arrangement, case)


        # run through athena

        avl_runner = avl.AVLRunner()
        avl_runner.setup_analysis(self.wing_file,
                                  self.mass_file,
                                  self.run_file)
        results = avl_runner.generate_results(self. results_dir)
        print(results)



if __name__ == "__main__":
    unittest.main()
