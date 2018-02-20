from os.path import join, exists, dirname, abspath
from os import makedirs, remove
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.aerodynamics as aero
from uav_design_system import aerofoil, layout
import uav_design_system.aerodynamics.athena_vortex_lattice as avl
import tempfile
import shutil

class TestAnalysis(unittest.TestCase):

    def create(self):

        # create a surface file ------------------------------------------------
        surface = avl.Surface("main")
        surface.define_mesh(20, 30, 1.0, 1.0)

        cord1 = 0.8
        section1 = avl.Section(cord1)
        section1.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.2, 0.5, 0)

        cord2 = 0.3
        section2 = avl.Section(cord2)
        section2.translation_bias(cord1  - cord2, 0.3, 0)
        section2.twist_angle = -1
        section2.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.2, 0.5, 0)

        cord3 = 0.05
        section3 = avl.Section(cord3)
        section3.twist_angle = -1
        section3.translation_bias(cord1 - cord3, 0.85, 0)
        section3.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.2, 0.5, 0)

        control_surface = avl.ControlSurface("elevator", 0.3, [0, 1, 0], avl.ControlDeflectionType.SYMMETRIC)
        surface.add_section(section1, section2, section3)
        surface.add_control_surface(control_surface, 1, 2)
        surface.reflect_surface = True
        plane = avl.Plane("UAV", surface)

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

        return plane, case, arrangement

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test_result_type(self):
        self.assertIsInstance(self.result, aero.AerodynamicStudy)

    def test_total_drag(self):
        self.plane, self.case, self.mass = self.create()
        self.result = aero.AerodynamicAnalysis.run(self.plane, self.case, self.mass)
        self.assertEqual(self.result.viscous_drag_coefficient, 0.017256236044657095)
        self.assertEqual(self.result.total_drag_coefficient, 0.11138 + 0.017256236044657095)

    def _test_total_drag_slow(self):
        self.plane, self.case, self.mass = self.create()
        self.case["velocity"] = 16
        self.result = aero.AerodynamicAnalysis.run(self.plane, self.case, self.mass)
        self.assertAlmostEqual(self.result.viscous_drag_coefficient, 0.0404, 4)
        self.assertAlmostEqual(self.result.total_drag_coefficient, 0.4620, 4)




if __name__ == "__main__":
    unittest.main()
