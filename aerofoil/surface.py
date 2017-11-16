"""
"""
import bezier



class Surface():
    """
    Class that represents a Surface from a number of nodes and degree
    """

    def __init__(self, nodes, degree: int = 2):
        self.nodes = nodes
        self.degree = degree

    def generate_bezier(self):
        """
        create a bezier curve class from the nodes
        """
        return bezier.Curve(self.nodes, degree = self.degree)
