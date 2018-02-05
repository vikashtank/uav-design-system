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

        self.plot = True

    def tearDown(self):
        rmtree(self.results_dir)
        rmtree(self.test_folder)

    def create(self, input_dict, name  = "UAV"):

        surface = avl.Surface("main_wing")
        surface.define_mesh(15, 20, 1.0, 1.0)

        main_cord1 = input_dict["cord_1"]
        section1 = avl.Section(main_cord1)
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
        section2.translation_bias(main_cord1  - cord2 - wing_shift_1, input_dict["span_section_1"], 0)
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
        section3.translation_bias(main_cord1 - cord3 - wing_shift_1 - wing_shift_2, input_dict["span_section_2"], 0)
        thickness = input_dict["aerofoil_3_thickness"]
        section3.aerofoil = aerofoil.Aerofoil.develop_aerofoil(thickness,
                                                               -1 * thickness,
                                                               input_dict["aerofoil_3_camber"],
                                                               input_dict["aerofoil_3_thickness_loc"],
                                                               input_dict["aerofoil_3_camber"])


        surface.add_section(section1, section2, section3)
        surface.reflect_surface = True

        # design tail
        tail_surface = avl.Surface("tail")
        tail_surface.define_translation_bias(input_dict["elevator_distance"], 0, 0)
        tail_surface.define_mesh(10, 15, 1.0, 1.0)
        thickness = input_dict["tail_thickness"]
        tail_aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.5*thickness,
                                                       -1 * 0.5*thickness,
                                                       input_dict["tail_thickness"],
                                                       input_dict["tail_thickness_loc"],
                                                       input_dict["tail_camber"])
        cord1 = input_dict["tail_cord_1"]
        tail_section1 = avl.Section(cord1)
        tail_section1.aerofoil = tail_aerofoil

        cord2 = input_dict["tail_cord_2"]
        tail_section2 = avl.Section(cord2)
        tail_section2.translation_bias(0, input_dict["boom_width"]*0.5, 0)
        tail_section2.aerofoil = tail_aerofoil

        cord3 = input_dict["tail_cord_3"]
        tail_section3 = avl.Section(cord3)
        tail_section3.translation_bias(0, input_dict["boom_width"]*0.5 + input_dict["elevator_span"], 0)
        tail_section3.aerofoil = tail_aerofoil

        tail_surface.add_section(tail_section1, tail_section2, tail_section3)
        tail_surface.reflect_surface = True
        control_surface = avl.ControlSurface("elevator", input_dict["elevator_size"], [0, 1, 0], avl.ControlDeflectionType.SYMMETRIC)
        tail_surface.add_control_surface(control_surface, 0, 2)
        # create a mass file ---------------------------------------------------
        # create sustructure from wing
        structure_creator  = layout.StructureFactory(layout.StructuralModelType.HOLLOWFOAM)
        structural_model = structure_creator(surface, wall_thickness = input_dict["wall_thickness"])
        structural_clone =  structural_model.clone(reflect_y = True)

        # create structure for tail
        tail_structural_model = structure_creator(tail_surface, wall_thickness = input_dict["tail_wall_thickness"])
        tail_structural_model.location = layout.Point(tail_surface.x, tail_surface.y, tail_surface.z)
        tail_structural_clone =  tail_structural_model.clone(reflect_y = True)

        # add some more weights and arrangement
        battery = layout.MassObject(layout.Cuboid(0.1, 0.1, 0.1), 1)
        battery.location = layout.Point(input_dict["battery_x_loc"] * main_cord1, -0.05, -0.05)

        motor = layout.MassObject(layout.Cuboid(0.1, 0.1, 0.1), 1)
        motor.location = layout.Point(main_cord1, -0.05, -0.05)

        arrangement = layout.Arrangement("plane arrangement", battery,
                                                              motor,
                                                              structural_model,
                                                              structural_clone,
                                                              tail_structural_model,
                                                              tail_structural_clone)

        # create case file -----------------------------------------------------
        case = avl.TrimCase(surface.area * 2, velocity = 22,
                            mass = arrangement.total_mass)

        plane = avl.Plane(name, surface, tail_surface)

        return plane, case, arrangement

    def uav_dict(self, **kwargs):
        uav_dict = {
            "cord_1": 0.42,
            "cord_2": 0.42,
            "span_section_1": 0.2,
            "cord_3": 0.42,
            "span_section_2": 0.9,
            "elevator_size": 0.1,
            "battery_x_loc": 0,
            "wall_thickness": 0.09,
            "aerofoil_1_thickness": 0.15,
            "aerofoil_1_camber": 0.02,
            "aerofoil_1_thickness_loc": 0.295,
            "aerofoil_2_thickness": 0.15,
            "aerofoil_2_camber": 0.02,
            "aerofoil_2_thickness_loc": 0.295,
            "aerofoil_3_thickness": 0.15,
            "aerofoil_3_camber": 0.02,
            "aerofoil_3_thickness_loc": 0.295,
            "twist_angle_2": 0,
            "twist_angle_3": 0,
            "wing_shift_1": 0,
            "wing_shift_2": 0,
            "elevator_span": 0.2,
            "boom_width": 0.4,
            "elevator_distance": 0.7,
            "tail_thickness": 0.12,
            "tail_thickness_loc": 0.12,
            "tail_camber": 0,
            "tail_cord_1": 0.1,
            "tail_cord_2": 0.1,
            "tail_cord_3": 0.1,
            "tail_wall_thickness": 0.05,
        }
        uav_dict.update(kwargs)
        return uav_dict

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

    def display_results(self, title, results):
        print(title)
        print("alpha ", results.alpha)
        print("elevator deflection ", results.elevator_deflection)
        print("cl ", results.cl)
        print("cd ", results.cd)
        print("stability ", results.neutral_point)
        print("cl/cd ", results.cl/ results.cd)
        print("")


    def test_run_cruise(self):

        uav_dict = self.uav_dict()
        plane, case, arrangement = self.create(uav_dict)
        avl, aero, case, mass = self.generate_files(plane, case, arrangement)
        results = self.analyse(avl, aero, case, mass)
        self.display_results("cruise", results)


        if self.plot:
            plt.figure(1)
            plot = plt.subplot(111)
            plane.plot_xy(plot, "g_")
            arrangement.plot_xy(plot, True, "r-")

            plt.figure(2)
            plot = plt.subplot(111)
            plane.surfaces[0][0].aerofoil.plot(plot)

            plt.figure(3)
            plot = plt.subplot(111)
            plane.surfaces[1][0].aerofoil.plot(plot)

            plt.axes().set_aspect('equal')
            plt.show()

    def test_run_landing(self):

        uav_dict = self.uav_dict()
        plane, case, arrangement = self.create(uav_dict)
        case["velocity"] = 9
        avl, aero, case, mass = self.generate_files(plane, case, arrangement)
        results = self.analyse(avl, aero, case, mass)
        self.display_results("landing", results)




if __name__ == "__main__":
    unittest.main()
