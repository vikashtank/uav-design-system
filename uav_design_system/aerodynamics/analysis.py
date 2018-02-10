"""
file that provides an interface between the surface class, athena vortex lattice and xfoil
"""
from os.path import join, exists, dirname, abspath
from os import makedirs, remove
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
from uav_design_system import layout, aerodynamics as aero
import tempfile
import shutil
from scipy.integrate import quad

class Inputs():

    def __init__(self, plane, case, arrangement):
        self.plane = plane
        self.case = case
        self.arrangement = arrangement

class Results():

    def __init__(self, xfoil_results, avl_results):
        self.xfoil_results = xfoil_results
        self.avl_results = avl_results


class AerodynamicStudy():

    def __init__(self, inputs: Inputs, results: Results):
        self.inputs = inputs
        self.results = results

    @property
    def dynamic_pressure(self):
        case = self.inputs.case
        return 0.5 * case["density"] * (case["velocity"] **2)


    @property
    def viscous_drag_coefficient(self) -> float:
        """
        calculates total drag of plane
        """
        drag = 0
        for index, surface in enumerate(self.inputs.plane):
            drag += self._calc_surface_drag(self.results.xfoil_results[index],
                                            surface)

        # non dimenionalise (alread per unit dynamic pressure)
        drag_coefficient = drag/(self.inputs.plane.main_surface.area)

        return drag_coefficient

    @property
    def total_drag_coefficient(self):
        return self.viscous_drag_coefficient + self.results.avl_results.cd

    def _calc_surface_drag(self, xfoil_results, surface):
        """
        calculate the drag per dynamic pressure between two sections
        """
        drag = 0
        for index in range(len(surface) - 1) :
            drag += self._get_section_drag(xfoil_results,
                                           index,
                                           surface[index],
                                           surface[index + 1])
        # times drag by two if surface is reflected
        if surface.reflect_surface:
            drag = drag * 2

        return drag

    def _get_section_drag(self, xfoil_results, index, section, next_section):
        """
        get drag per dynamic pressure between two sections
        """
        cd, cord, y = xfoil_results[index]["cd"], section.cord, section.y
        cd2, cord2, y2 = xfoil_results[index + 1]["cd"], next_section.cord, next_section.y
        span = y2 - y
        mc = (cord2 - cord) / span
        mv = (cd2 - cd) / span
        return self._integrate( mc*mv, cord*mv + cd*mc, cord*cd, span)

    def _integrate(self, coeff1, coeff2, coeff3, span):
        """
        analytic function for the calculation of viscous drag per dynamic
        pressure along a section.
        assuming linear interpolation of viscous drag coefficients between sections
        """
        return (coeff1 * (1/3) * span**3) +  (coeff2 * 0.5 * span**2) + coeff3 * span



class AerodynamicAnalysis():

    def __init__(self, plane, case, arrangement):
        self.plane = plane
        self.case = case
        self.arrangement = arrangement

        #set xfoil path
        self.xfoil_file_path = "/Applications/Xfoil.app/Contents/Resources/xfoil"
        self.xfoil_results_dir = tempfile.mkdtemp()

        #setup athena_vortex_lattice
        self.athena_results_dir = tempfile.mkdtemp()

    def __del__(self):
        shutil.rmtree(self.xfoil_results_dir)
        shutil.rmtree(self.athena_results_dir)

    def _run_avl(self):
        avl_file, aerofoil_files, case_file, mass_file = self._generate_avl_files(self.plane,
                                                                                 self.case,
                                                                                 self.arrangement)
        avl_runner = aero.athena_vortex_lattice.AVLRunner()
        avl_runner.setup_analysis(avl_file,
                                       mass_file,
                                       case_file,
                                       *aerofoil_files)
        return avl_runner.generate_results(self.athena_results_dir)

    def _generate_avl_files(self, plane, case, arrangement):
        run_file = join(self.athena_results_dir, "run.avl")
        case.to_file(run_file)
        mass_file = join(self.athena_results_dir, "mass.mass")
        layout.create_mass_file(mass_file, arrangement, case)
        avl_input, aerofoil_files = plane.dump_avl_files(self.athena_results_dir)
        return avl_input, aerofoil_files, run_file, mass_file

    def _run_xfoil(self, aerofoil_file, aerofoil, angle_of_attack, reynolds_number):
        with open(aerofoil_file, "w") as open_file:
            aerofoil.write(open_file)
        xfoil_runner = aero.xfoil.XfoilRunner(self.xfoil_file_path)
        xfoil_runner.setup_analysis(aerofoil_file, reynolds_number)
        return xfoil_runner(angle_of_attack - 2, angle_of_attack + 1, 0.5, False).get_alpha(angle_of_attack)

    def _run_xfoil_plane(self, alpha):
        xfoil_results = {}
        for i, surface in enumerate(self.plane):
            surf_dict = {}
            xfoil_results[i] = surf_dict
            for j, section in enumerate(surface):
                angle_of_attack = section.twist_angle + alpha
                # calc reynolds number
                reynolds_number = (self.case["density"] * self.case["velocity"] * section.cord)/ (1.983e-5)
                # create aerofoil_file_name
                aerofoil_file_name = join(self.xfoil_results_dir, f"surf{i}_sec{j}_af.txt")
                result = self._run_xfoil(aerofoil_file_name,
                                         section.aerofoil,
                                         angle_of_attack,
                                         reynolds_number)
                # return results dictionary
                surf_dict[j] = result
        return xfoil_results

    def _run_analysis(self):
        # run avl
        avl_results = self._run_avl()
        # run xfoil
        xfoil_results = self._run_xfoil_plane(avl_results.alpha)
        return xfoil_results, avl_results

    @staticmethod
    def run(plane, case, arrangement) -> AerodynamicStudy:
        analyser = AerodynamicAnalysis(plane, case, arrangement)
        xfoil_results, avl_results = analyser._run_analysis()

        input = Inputs(plane, case, arrangement)
        output = Results(xfoil_results, avl_results)
        return AerodynamicStudy(input, output)







if __name__ == "__main__":
    pass
