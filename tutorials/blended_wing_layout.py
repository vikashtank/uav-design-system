"""
Integration test to ensure that AVL accepts the case, plane and mass files
created
"""
from os.path import join, exists, dirname, abspath
from os import makedirs
from shutil import rmtree
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../")  # so uggo thanks to atom runner
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

        self.alphas = []
        self.eff = []
        self.landing_alpha = []
        self.cl_cd = []

        self.run_analysis = True
        self.plot = False

    def tearDown(self):
        rmtree(self.results_dir)
        rmtree(self.test_folder)

    def create(self, input_dict, name  = "UAV"):

        surface = avl.Surface("main_wing")
        surface.define_mesh(20, 30, 1.0, 1.0)

        cord1 = input_dict["cord_1"]
        section1 = avl.Section(cord1)
        thickness = input_dict["aerofoil_1_thickness"]
        section1.aerofoil = aerofoil.Aerofoil.develop_aerofoil(thickness,
                                                               -1 * thickness,
                                                               input_dict["aerofoil_1_thickness"],
                                                               input_dict["aerofoil_1_thickness_loc"],
                                                               input_dict["aerofoil_1_camber"])

        cord2 = input_dict["cord_2"]
        section2 = avl.Section(cord2)
        section2.twist_angle = input_dict["twist_angle_2"]
        wing_shift_1 = input_dict["wing_shift_1"]
        section2.translation_bias(cord1  - cord2 - wing_shift_1, input_dict["span_section_1"], 0)
        thickness = input_dict["aerofoil_2_thickness"]
        section2.aerofoil = aerofoil.Aerofoil.develop_aerofoil(thickness,
                                                               -1 * thickness,
                                                               input_dict["aerofoil_2_thickness"],
                                                               input_dict["aerofoil_2_thickness_loc"],
                                                               input_dict["aerofoil_2_camber"])

        cord3 = input_dict["cord_3"]
        section3 = avl.Section(cord3)
        section3.twist_angle = input_dict["twist_angle_3"]
        wing_shift_2 = input_dict["wing_shift_2"]
        section3.translation_bias(cord1 - cord3 - wing_shift_1 - wing_shift_2, input_dict["span_section_2"], 0)
        thickness = input_dict["aerofoil_3_thickness"]
        section3.aerofoil = aerofoil.Aerofoil.develop_aerofoil(thickness,
                                                               -1 * thickness,
                                                               input_dict["aerofoil_3_camber"],
                                                               input_dict["aerofoil_3_thickness_loc"],
                                                               input_dict["aerofoil_3_camber"])

        control_surface = avl.ControlSurface("elevator", input_dict["elevator_size"], [0, 1, 0], avl.ControlDeflectionType.SYMMETRIC)
        surface.add_section(section1, section2, section3)
        surface.add_control_surface(control_surface, 1, 2)
        surface.reflect_surface = True

        # create a mass file ---------------------------------------------------
        # create sustructure from wing
        structure_creator  = layout.StructureFactory(layout.StructuralModelType.HOLLOWFOAM)
        structural_model = structure_creator(surface, wall_thickness = input_dict["wall_thickness"])
        structural_clone =  structural_model.clone(reflect_y = True)

        # add some more weights and arrangement
        battery = layout.MassObject(layout.Cuboid(0.1, 0.1, 0.1), 1)
        battery.location = layout.Point(input_dict["battery_x_loc"] * cord1, -0.05, -0.05)

        motor = layout.MassObject(layout.Cuboid(0.1, 0.1, 0.1), 1)
        motor.location = layout.Point(cord1, -0.05, -0.05)

        arrangement = layout.Arrangement("plane arrangement", battery, motor, structural_model, structural_clone)

        # create case file -----------------------------------------------------
        case = avl.TrimCase(surface.area * 2, velocity = 22,
                            mass = arrangement.total_mass)

        plane = avl.Plane(name, surface)

        return plane, case, arrangement


    def uav_dict(self, **kwargs):
        uav_dict = {
            "cord_1": 0.8,
            "cord_2": 0.2,
            "span_section_1": 0.3,
            "cord_3": 0.05,
            "span_section_2": 0.85,
            "elevator_size": 0.3,
            "battery_x_loc": 0,
            "wall_thickness": 1,
            "aerofoil_1_thickness": 0.2,
            "aerofoil_1_camber": 0,
            "aerofoil_1_thickness_loc": 0.5,
            "aerofoil_2_thickness": 0.2,
            "aerofoil_2_camber": 0,
            "aerofoil_2_thickness_loc": 0.5,
            "aerofoil_3_thickness": 0.2,
            "aerofoil_3_camber": 0,
            "aerofoil_3_thickness_loc": 0.5,
            "twist_angle_2": 0,
            "twist_angle_3": 0,
            "wing_shift_1": 0.1,
            "wing_shift_2": 0.1
        }
        uav_dict.update(kwargs)
        return uav_dict

    def display_results(self, title, results):
        print(title)
        print("alpha ", results.alpha)
        print("elevator deflection ", results.elevator_deflection)
        print("")

    def analyse(self, avl_file, aero, case, mass):
        avl_runner = avl.AVLRunner()
        avl_runner.setup_analysis(avl_file,
                                  mass,
                                  case,
                                  *aero)
        return avl_runner.generate_results(self.results_dir)

    def generate_files(self, plane, case, arrangement):
        case.to_file(self.run_file)
        layout.create_mass_file(self.mass_file, arrangement, case)
        avl_input, aerofoil_files = plane.dump_avl_files(self.test_folder)
        return avl_input, aerofoil_files, self.run_file, self.mass_file

    def test_run_study(self):

        uav_dict = self.uav_dict(cord_1 = 0.9, span_section_2 = 1.3)
        plane, case, arrangement = self.create(uav_dict)
        avl, aero, case, mass = self.generate_files(plane, case, arrangement)
        results = self.analyse(avl, aero, case, mass)

        self.display_results("cruise", results)

        if self.plot:
            plt.figure(1)
            plot = plt.subplot(111)
            plane.plot_xy(plot, "g_")
            arrangement.plot_xy(plot, True, "r-")
            plt.show()


    def _test_run_low_speed(self):
        uav_dict = self.uav_dict(cord_1 = 0.9, span_section_2 = 1.3, aerofoil_2_camber = 0.1)
        plane, case, arrangement = self.create(uav_dict)
        case["velocity"] = 9
        avl, aero, case, mass = self.generate_files(plane, case, arrangement)
        print(aero)
        results = self.analyse(avl, aero, case, mass)


    def _test_run_very_low_speed(self):
        uav_dict = self.uav_dict(cord_1 = 0.9, span_section_2 = 1.3)
        plane, case, arrangement = self.create(uav_dict)
        case["velocity"] = 7
        avl, aero, case, mass = self.generate_files(plane, case, arrangement)
        results = self.analyse(avl, aero, case, mass)





if __name__ == "__main__":
    unittest.main()
