"""
file for construting the genetic algorithm for use in this project
"""
import os
import shutil
import tempfile
from abc import ABC, abstractmethod
from .schema import Schema
import random
import collections
from typing import List, Dict



class Child():

    def __init__(self, inputs: Dict[str, float]):
        self.inputs = inputs


class GeneticFactory(ABC):
    pass


class Genetic():


    def __init__(self, factory: GeneticFactory, schema: Schema):
        self.factory = factory
        self.schema = schema


    def fitness(self, child: Child) -> float:
        """
        results a value for each child depending on how well it fits a function
        specified in this method.
        lower the value returned the better
        """
        return id(child)

    def generate_initial_population(self, population_size: int):
        """
        generate many potential designs for the initial run
        """
        population = []

        while(len(population) < population_size):
            child = self._create_random_child()
            if self.is_valid_child(child):
                population.append(child)

        return population

    def is_valid_child(self, child: Child):
        """
        checks the child created
        """
        # test that the sections fit the aerofoils
        return True

    def filter_population(self, population: List[Child]) -> List[Child]:
        """
        filters the population on how well they perform
        """
        half_size = int(0.5 * len(population))
        population.sort(key = lambda x: self.fitness(x))
        best_children = population[0: half_size]
        return best_children

    def _mutate(self, kwargs: Dict[str, float]) -> Dict[str, float]:
        """
        mutate the kwarg dictionary according to schema
        """
        new_dict = {}
        for key, value in kwargs.items():
            constraint = self.schema[key] # assume schema contains keys in input dict
            delta = 0.01 * (constraint.max - constraint.min)
            sign = random.choice([1, -1])
            new_value = value + sign * delta
            #enforce schema constraints
            new_dict[key] = self._confine(new_value, constraint.min, constraint.max)
        return new_dict

    def _confine(self, value, min, max):
        """
        confines values between minumin and maximum values
        """
        if value < min:
            value = min
        elif value > max:
            value = max
        return value

    def run_genetic(self, initial_population: List[Child],
                          current_generation: int,
                          max_generations: int) -> List[Child]:
        """
        takes an intial population and returns
        """
        children = initial_population

        if current_generation < max_generations - 1:
            best_children = self.filter_population(initial_population)
            next_population = self.generate_next_population(best_children)
            children = children + self.run_genetic(next_population,
                                                   current_generation + 1,
                                                   max_generations)
        return children

    def generate_next_population(self, population: List[Child]) -> List[Child]:
        """
        create a new population from the filtered population
        """
        new_population = []
        for i in range(len(population)):

            parent1 = population[i]
            parent2 = population[-i]
            child = self.child_from_parents(parent1, parent2)
            new_population.append(child)
            child = self.child_from_parents(parent2, parent1)
            new_population.append(child)

        return new_population

    def _combine(self, dict1: Dict[str, float],
                       dict2: Dict[str, float]) -> Dict[str, float]:
        """
        takes two children, and combines their input dictionaries to create
        a new child
        """
        dict3 = {}
        for index, key in enumerate(dict1):
            if index%2 == 0:
                dict3[key] = dict1[key]
            else:
                dict3[key] = dict2[key]
        return dict3

    def child_from_parents(self, parent1: Child, parent2: Child) -> Child:
        """
        create a child from two parents and mutate the child to produce
        next generation
        """
        combined_dict = self._combine(parent1.inputs, parent2.inputs)
        return Child(self._mutate(combined_dict))

    def _create_random_child(self) -> Child:
        """
        creates a random dictionary within the schema constraints
        """
        new_child_dict = {}
        for constraint in self.schema:
            val = random.uniform(constraint.min, constraint.max)
            val = round(val, 4)
            new_child_dict[constraint.name] = val

        return Child(new_child_dict)

    def __call__(self, generations = 10, store = False, display = False):
        initial_population = self.generate_initial_population(generations)
        return self.run_genetic(initial_population, 0, generations)


class PlaneChild(Child):
    pass


class AircraftGenetic(Genetic):

    def fitness(self, child: Child):
        """
        give designs a value between 0 for best and 100 for worse
        """

        results = self.analyse(child)
        return (results.cl/results.cd)

    def create(self, input_dict, name  = "UAV"):
        """
        takes a dictionary and creates the objects to analyse
        """
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

        return surface, case, arrangement

    def is_valid_child(self, child: Child):
        """
        checks the child created
        """
        # test that the sections fit the aerofoils
        return True

    def analyse(self, child: Child):
        # create temporary folder
        temp_folder =tempfile.mkdtemp()
        run_file = os.path.join(temp_folder, "run_file.case")
        mass_file = os.path.join(temp_folder, "mass.mass")


        # run analysis on sections
        case.to_file(run_file)
        layout.create_mass_file(mass_file, arrangement, case)
        avl_input, aerofoil_files = surface.dump_avl_inputs(temp_folder)

        avl_runner = avl.AVLRunner()
        avl_runner.setup_analysis(avl_file,
                                  mass,
                                  case,
                                  *aero)
        results = avl_runner.generate_results(self.results_dir)
        # delete temporary folder
        shutil.rmtree(temp_folder)

        return results, weight,

















if __name__ == "__main__":
    pass
