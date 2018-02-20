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
from uav_design_system import layout, aerofoil, aerodynamics as aero
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

        # design verticle_tail
        """
        vtail_surface = avl.Surface("verticle_tail")
        vtail_surface.define_translation_bias(input_dict["elevator_distance"], 0, 0)
        vtail_surface.define_mesh(10, 15, 1.0, 1.0)

        cord1 = input_dict["vtail_cord_1"]
        vtail_section1 = avl.Section(cord1)
        vtail_section1.translation_bias(0, input_dict["boom_width"]*0.5, 0)
        vtail_section1.aerofoil = tail_aerofoil

        cord2 = input_dict["vtail_cord_2"]
        vtail_section2 = avl.Section(cord2)
        vtail_section2.translation_bias(0, input_dict["boom_width"]*0.5, input_dict["vtail_height"])
        tail_section2.aerofoil = tail_aerofoil

        vtail_surface.add_section(vtail_section1, vtail_section2)
        vtail_surface.reflect_surface = True
        """

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
        battery = layout.MassObject.from_mass(layout.Cuboid(0.19, 0.035, 0.07), 0.306)
        battery.location = layout.Point(input_dict["battery_x_loc"] * main_cord1, -0.05, -0.05)
        battery2 = battery.clone(reflect_y = True)

        motor = layout.MassObject.from_mass(layout.Cuboid(0.092, 0.042, 0.042), 0.231)
        motor.location = layout.Point(-0.092, input_dict["span_section_2"], -0.05)
        motor2 = motor.clone(reflect_y = True)

        # motor controller
        motor_controller = layout.MassObject.from_mass(layout.Cuboid(0.08, 0.017, 0.031), 0.08)
        motor_controller.location = layout.Point(main_cord1, -0.05, -0.05)

        # add landing gear
        landing_gear = layout.MassObject.from_mass(layout.Cuboid(0.105, 0.05, 0.065), 0.147)
        landing_gear.location = layout.Point(0.6*main_cord1, input_dict["span_section_2"], -0.05)
        landing_gear2 = landing_gear.clone(reflect_y = True)
        #oleo struts


        # add two hollow booms
        boom1 = layout.MassObject.from_mass(layout.HollowCylinder(0.012, 0.9, 0.005), 0.02727)
        boom1.location = layout.Point(0.25*main_cord1, -0.05, -0.05)
        boom1_ref = boom1.clone(reflect_y = True)

        boom2 = layout.MassObject(layout.HollowCylinder(0.012, 0.9, 0.005), 0.02727)
        boom2.location = layout.Point(0.6*main_cord1, -0.05, -0.05)
        boom2_ref = boom2.clone(reflect_y = True)

        # add horizontal booms
        horizontal_boom1 = layout.MassObject.from_mass(layout.Cuboid( 1.2, 0.012, 0.012), 0.03636)
        horizontal_boom1.location = layout.Point(-0.5, 0.1, 0)
        horizontal_boom2 = horizontal_boom1.clone(reflect_y = True)

        # wing box
        box = layout.MassObject.from_mass(layout.Cuboid( 0.42, 0.05, 0.05), 0.231)
        box.location = layout.Point(0, input_dict["span_section_2"], 0)
        box2 = box.clone(reflect_y = True)

        # fuselage box
        fuselage = layout.MassObject.from_mass(layout.Cuboid(0.852, 0.15, 0.15), 0.171)
        fuselage.location = layout.Point(-0.5, -0.15*0.5, 0)


        #servos, wires, computer,

        arrangement = layout.Arrangement("plane arrangement", battery,
                                                              battery2,
                                                              motor, motor2,
                                                              landing_gear, landing_gear2,
                                                              boom1, boom1_ref,
                                                              boom2, boom2_ref,
                                                              box, box2,
                                                              fuselage,
                                                              horizontal_boom1, horizontal_boom2,
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
            "span_section_2": 0.8,
            "elevator_size": 0.5,
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
            "elevator_span": 0.1,
            "boom_width": 0.2,
            "elevator_distance": 0.7,
            "tail_thickness": 0.12,
            "tail_thickness_loc": 0.12,
            "tail_camber": 0,
            "tail_cord_1": 0.1,
            "tail_cord_2": 0.1,
            "tail_cord_3": 0.1,
            "tail_wall_thickness": 0.05,
            "vtail_cord_1": 0.1,
            "vtail_cord_2": 0.05,
            "vtail_height": 0.2,
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
        print("cl ", results.cl*2)
        print("cd ", results.cd*2)
        print("stability ", results.neutral_point)

    def _test_run_cruise(self):
        uav_dict = self.uav_dict()
        plane, case, arrangement = self.create(uav_dict)
        analysis_case = aero.AerodynamicAnalysis.run(plane, case, arrangement)
        self.display_results("cruise", analysis_case.results.avl_results)
        print("total mass ", arrangement.total_mass)
        print("tot_drag ", analysis_case.total_drag_coefficient )
        print("ref area ", plane.main_surface.area)
        print("")

    def _test_longer_tail(self):
        uav_dict = self.uav_dict(elevator_distance = 1.1)
        plane, case, arrangement = self.create(uav_dict)
        analysis_case = aero.AerodynamicAnalysis.run(plane, case, arrangement)
        self.display_results("longer tail", analysis_case.results.avl_results)
        print("total mass ", arrangement.total_mass)
        print("tot_drag ", analysis_case.total_drag_coefficient )
        print("cl/cd ", analysis_case.results.avl_results.cl/ analysis_case.total_drag_coefficient.cd)
        print("ref area ", plane.main_surface.area)
        print("")

    def _test_higherAr_tail(self):
        uav_dict = self.uav_dict(elevator_distance = 1.1, elevator_span = 0.2)
        plane, case, arrangement = self.create(uav_dict)
        analysis_case = aero.AerodynamicAnalysis.run(plane, case, arrangement)
        self.display_results("longer tail higher AR", analysis_case.results.avl_results)
        print("total mass ", arrangement.total_mass)
        print("tot_drag ", analysis_case.total_drag_coefficient )
        print("ref area ", plane.main_surface.area)
        print("")

    def test_higherAr_tail(self):
        uav_dict = self.uav_dict(elevator_distance = 1.3, elevator_span = 0.1, tail_cord_1 = 0.1, tail_cord_2 = 0.1, tail_cord_3 = 0.1)
        plane, case, arrangement = self.create(uav_dict)
        analysis_case = aero.AerodynamicAnalysis.run(plane, case, arrangement)
        self.display_results("longer tail higher AR", analysis_case.results.avl_results)
        print("total mass ", arrangement.total_mass)
        print("cog ", arrangement.center_of_gravity)
        print("tot_drag ", analysis_case.total_drag_coefficient )
        print("cl/cd ", analysis_case.results.avl_results.cl*2/ analysis_case.total_drag_coefficient)
        print("ref area ", plane.main_surface.area)
        print("")
        self._plot(plane, case, arrangement)


    def _test_run_landing(self):

        uav_dict = self.uav_dict()
        plane, case, arrangement = self.create(uav_dict)
        case["velocity"] = 9
        analysis_case = aero.AerodynamicAnalysis.run(plane, case, arrangement)
        self.display_results("landing", analysis_case.results.avl_results)
        print("tot_drag ", analysis_case.total_drag_coefficient )
        print("ref area ", plane.main_surface.area)
        print(arrangement.total_mass)

    def _plot(self, plane, case, arrangement):
        uav_dict = self.uav_dict()

        plt.figure(1)
        plot = plt.subplot(111)
        plane.plot_xy(plot, "g_")
        arrangement.plot_xy(plot, True, "r-")
        plt.show()


if __name__ == "__main__":
    unittest.main()
