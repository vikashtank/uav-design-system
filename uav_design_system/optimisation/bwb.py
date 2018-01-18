"""
factory class for creating a BWB aircraft factory
"""
from os.path import dirname, abspath, join
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")
from uav_design_system import layout, aerofoil, athena_vortex_lattice as avl
from uav_design_system.optimisation import genetic
import json
from matplotlib import pyplot as plt


class BWBFactory(genetic.Genetic):

    def __init__(self, schema):
        self.schema = schema

    def __call__(self, input_dict, name):
        self.input_dict = input_dict
        # check input dict against schema
        self._check_against_schema(input_dict)
        # create aircraft from dict
        return create_wing(input_dict, name = name)

    def analyse(self, surface):
        pass

    def create_child(self):
        print("hello")

def create(input_dict, name = "uav"):

    surface = avl.Surface(name)
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

    return surface, arrangement, case


    case.to_file(self.run_file)
    layout.create_mass_file(self.mass_file, arrangement, case)

if __name__ == "__main__":
    """
    uav_dict_file = join(this_directory, "uav.json")
    with open(uav_dict_file) as open_file:
        print(open_file.read())
        uav_dict = json.load(open_file)
    print(uav_dict)
    """

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
        "aerofoil_1_camber": 0.2,
        "aerofoil_1_thickness_loc": 0.5,
        "aerofoil_2_thickness": 0.2,
        "aerofoil_2_camber": 0.2,
        "aerofoil_2_thickness_loc": 0.5,
        "aerofoil_3_thickness": 0.2,
        "aerofoil_3_camber": 0.2,
        "aerofoil_3_thickness_loc": 0.5,
        "twist_angle_2": 0,
        "twist_angle_3": 0,
        "wing_shift_1": 0.1,
        "wing_shift_2": 0.1
    }

    surface, _, _ = create(uav_dict, "hey")
    surface.plot_xy(marker = "r")
    #plt.show()
