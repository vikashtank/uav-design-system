"""
Script for generating aerofoil files
"""
import bezier
import numpy as np
import matplotlib.pyplot as plt
from typing import List
import os

class Surface():

    def __init__(self, nodes, degree: int = 2):
        self.nodes = nodes
        self.degree = degree

    def generate_bezier(self):
        """
        create a bezier curve class from the nodes
        """
        return bezier.Curve(self.nodes, degree = self.degree)


class Aerofoil():

    def __init__(self, suction_surface: Surface, pressure_surface: Surface):
        self.suction_surface = suction_surface
        self.pressure_surface = pressure_surface

    def plot(self, num_points: int = 250):
        """
        Plots both the suction and pressure surface of this aerofoil

        Inputs:
            num_points: The resolution of the plot

        Returns:
            (ax object): A matplotlib ax object with the aerofoil plotted
        """
        suction_curve = self.suction_surface.generate_bezier()
        pressure_curve = self.pressure_surface.generate_bezier()

        plot = suction_curve.plot(num_points)
        pressure_curve.plot(num_points, ax = plot)

        return plot

    @staticmethod
    def develop_aerofoil(le_top: float, le_bottom: float, thickness: float,
                         camber_x: float, camber_y: float) -> Aerofoil:
        """
        generates an aerofoil from the parameters provided from 6 control points:
            1 control point at the leading edge
            1 at the trailing edge
            2 parallel in the y direction at the leading edge (above and below)
            2 middle points verticly alligned

        inputs:
            le_top:     The y coordinate of the suction surface curve point, x = 0
            le_bottom:  The y coordinate of the pressure surface curve point, x = 0
            thickness:  The distance between the two middle control points verticly
            camber_x:   The x position of both middle control points
            camber_y:   The y position added to both middle control points

        returns:
            Aerofoil:   Returns an aerofoil instance
        """
        mid_top = [camber_x, camber_y + thickness*0.5]
        mid_bottom = [camber_x, camber_y - thickness*0.5]

        nodes1 = np.asfortranarray([[0, 0], [0, le_top], mid_top, [1, 0]])
        nodes2 = np.asfortranarray([[0, 0], [0, le_bottom], mid_bottom, [1, 0]])

        s_surface = Surface(nodes1, 2)
        p_surface = Surface(nodes2, 2)
        aerofoil = Aerofoil(s_surface, p_surface)

        return aerofoil


    def write(self, open_file, number_nodes: int = 100):
        """
        writes the suction and pressure surface x,y coordinates into a file with
        a title line of the control nodes

        Inputs:
            open_file:  a file stream object
            number_nodes:  The number of points for each surface to be written

        Returns:
            None
        """
        nodes1 = self.pressure_surface.nodes
        nodes2 = self.suction_surface.nodes

        node1_str = str(nodes1).replace("\n", "").replace(" ", "")
        node2_str = str(nodes2).replace("\n", "").replace(" ", "")

        open_file.write("pressure surface: {0}, suction surface: {1}\n".format(node1_str, node2_str))

        points = np.linspace(0, 1, number_nodes)
        pressure_surface_points = self.pressure_surface.generate_bezier().evaluate_multi(points)
        suction_surface_points = self.suction_surface.generate_bezier().evaluate_multi(points)

        suction_surface_points = suction_surface_points[::-1]
        all_points = np.concatenate((suction_surface_points,pressure_surface_points))

        for i in all_points:
            open_file.write("{0} {1}\n".format(i[0], i[1]))



if __name__ == "__main__":

    array = [[1,0], [0., 0.], [0.5, 1.], [1., 0.]]

    aerofoil = Aerofoil.develop_aerofoil(0.1, -0.1, 0.2, 0.5, 0.)

    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(dir_name, "hey2.txt")


    with open(file_name, "w") as open_file:
        aerofoil.write(open_file)
