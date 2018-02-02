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
from uav_design_system import layout, aerofoil
from uav_design_system.aerodynamics import athena_vortex_lattice as avl
from matplotlib import pyplot as plt
import json


class Test(unittest.TestCase):

    def setUp(self):
        # make temporary folder
        self.test_folder = join(this_directory, "test_folder")
        makedirs(self.test_folder)

        self.results_dir = join(this_directory, "results")
        makedirs(self.results_dir)

        # create temporary file names
        self.mass_file = join(self.test_folder, "UAV.mass")
        self.run_file = join(self.test_folder, "UAV.run")

        self.run_analysis = True
        self.plot = False

    def tearDown(self):
        rmtree(self.results_dir)
        rmtree(self.test_folder)

    def test_integration(self):

        # create a surface file ------------------------------------------------
        surface = avl.Surface("UAV")
        surface.define_mesh(20, 30, 1.0, 1.0)

        cord1 = 0.8
        section1 = avl.Section(cord1)
        section1.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.2, 0.5, 0)

        cord2 = 0.3
        section2 = avl.Section(cord2)
        section2.translation_bias(cord1  - cord2, 0.3, 0)
        section2.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.2, 0.5, 0)

        cord3 = 0.05
        section3 = avl.Section(cord3)
        section3.translation_bias(cord1 - cord3, 0.85, 0)
        section3.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.2, 0.5, 0)

        control_surface = avl.ControlSurface("elevator", 0.3, [0, 1, 0], avl.ControlDeflectionType.SYMMETRIC)
        surface.add_section(section1, section2, section3)
        surface.add_control_surface(control_surface, 1, 2)
        surface.reflect_surface = True
        plane = avl.Plane("UAV", surface)

        avl_input, aerofoil_files = plane.dump_avl_files(self.test_folder)

        # create a mass file ---------------------------------------------------
        # create sustructure from wing
        structure_creator  = layout.StructureFactory(layout.StructuralModelType.HOLLOWFOAM)
        structural_model = structure_creator(surface, wall_thickness = 1)
        structural_clone =  structural_model.clone(reflect_y = True)

        # add some more weights and arrangement
        battery = layout.MassObject(layout.Cuboid(0.1, 0.1, 0.1), 1)
        battery.location = layout.Point(0, -0.05, -0.05)

        arrangement = layout.Arrangement("plane arrangement", battery, structural_model, structural_clone)

        # create case file -----------------------------------------------------
        case = avl.TrimCase(surface.area * 2, velocity = 22,
                            mass = arrangement.total_mass)
        case.to_file(self.run_file)
        layout.create_mass_file(self.mass_file, arrangement, case)

        # run through athena
        avl_runner = avl.AVLRunner()
        avl_runner.setup_analysis(avl_input,
                                  self.mass_file,
                                  self.run_file,
                                  *aerofoil_files)
        results = avl_runner.generate_results(self.results_dir)
        self.assertEqual(results.alpha, 1.29549)
        self.assertEqual(results.elevator_deflection, 2.80441)


        if self.plot:
            plot = plt.subplot(111)
            surface.plot_xy(plot, "g_")
            arrangement.plot_xy(plot, True, "r-")
            plt.show()

    def test_integration_change_aero(self):

        # create a surface file ------------------------------------------------
        surface = avl.Surface("UAV")
        surface.define_mesh(20, 30, 1.0, 1.0)

        cord1 = 0.8
        section1 = avl.Section(cord1)
        section1.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.3, 0.5, 0)

        cord2 = 0.3
        section2 = avl.Section(cord2)
        section2.translation_bias(cord1  - cord2, 0.3, 0)
        section2.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.2, 0.5, 0)

        cord3 = 0.05
        section3 = avl.Section(cord3)
        section3.translation_bias(cord1 - cord3, 0.85, 0)
        section3.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.2, 0.5, 0)

        control_surface = avl.ControlSurface("elevator", 0.3, [0, 1, 0], avl.ControlDeflectionType.SYMMETRIC)
        surface.add_section(section1, section2, section3)
        surface.add_control_surface(control_surface, 1, 2)
        surface.reflect_surface = True
        plane = avl.Plane("UAV", surface)

        avl_input, aerofoil_files = plane.dump_avl_files(self.test_folder)

        # create a mass file ---------------------------------------------------
        # create sustructure from wing
        structure_creator  = layout.StructureFactory(layout.StructuralModelType.HOLLOWFOAM)
        structural_model = structure_creator(surface, wall_thickness = 1)
        structural_clone =  structural_model.clone(reflect_y = True)

        # add some more weights and arrangement
        battery = layout.MassObject(layout.Cuboid(0.1, 0.1, 0.1), 1)
        battery.location = layout.Point(0, -0.05, -0.05)

        arrangement = layout.Arrangement("plane arrangement", battery, structural_model, structural_clone)

        # create case file -----------------------------------------------------
        case = avl.TrimCase(surface.area * 2, velocity = 22,
                            mass = arrangement.total_mass)
        case.to_file(self.run_file)
        layout.create_mass_file(self.mass_file, arrangement, case)

        # run through athena
        avl_runner = avl.AVLRunner()
        avl_runner.setup_analysis(avl_input,
                                  self.mass_file,
                                  self.run_file,
                                  *aerofoil_files)
        results = avl_runner.generate_results(self.results_dir)
        self.assertNotEqual(results.alpha, 1.29549)
        self.assertNotEqual(results.elevator_deflection, 2.80441)


        if self.plot:
            plot = plt.subplot(111)
            surface.plot_xy(plot, "g_")
            arrangement.plot_xy(plot, True, "r-")
            plt.show()





if __name__ == "__main__":
    unittest.main()
