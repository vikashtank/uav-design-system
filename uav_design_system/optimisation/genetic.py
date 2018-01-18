"""
file for construting the genetic algorithm for use in this project
"""
from abc import ABC, abstractmethod

class Genetic(ABC):


    def __init__(self, factory, factory_args, ):
        self.population_size = None

    def _fitness(self):
        pass

    def generate_first_population(self, population_size):
        """
        generate many potential designs for the initial run
        """
        self.population_size = population_size
        pass

    def mutate(self):
        """

        """
        pass

    @abstractmethod
    def create_child(self):
        pass

    def create_children(self):
        pass


class GeneticInterface(ABC):

    def __init__(self, schema = None):
        self.schema = schema

    @abstractmethod
    def _check_against_schema(self, input_dict):
        pass

    @abstractmethod
    def analyse(self, surface):
        pass

    def _check_input_dict_keys(self, input_dict):

        for key in self.schema:
            try:
                inut_dict[key]
            except AttributeError:
                pass



















if __name__ == "__main__":
    pass
