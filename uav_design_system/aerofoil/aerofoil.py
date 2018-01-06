"""
"""
import numpy as np
import bezier
import scipy.optimize as opt


class Aerofoil():
    """
    Class that represents an Aerofoil
    """

    def __init__(self, suction_surface: 'Surface', pressure_surface: 'Surface'):

        self.suction_surface = suction_surface
        self.pressure_surface = pressure_surface

    def plot(self, plot = None,num_points: int = 250, colour = "g"):
        """
        Plots both the suction and pressure surface of this aerofoil

        Inputs:
            ax: The axis to plot the coordinates on
            num_points: The resolution of the plot

        Returns:
            (ax object): A matplotlib ax object with the aerofoil plotted
        """
        suction_curve = self.suction_surface.bezier
        pressure_curve = self.pressure_surface.bezier

        if plot:
            pl = suction_curve.plot(num_points, ax = plot, color = colour)
            pressure_curve.plot(num_points, ax = plot, color = colour)
        else:
            plot = suction_curve.plot(num_points, color = colour)
            pressure_curve.plot(num_points, ax = plot, color = colour)

        return plot

    @staticmethod
    def develop_aerofoil(le_top: float, le_bottom: float, thickness: float,
                         camber_x: float, camber_y: float):
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


    def get_maxmin_y(self, x_target: float, **kwargs):
        """
        gets the top surface y coordinate and bottom surface y coordinate at a
        given x
        """

        y_pressure, _ = self.pressure_surface.get_y(x_target, **kwargs)
        y_suction, _ = self.suction_surface.get_y(x_target, **kwargs)

        return  y_pressure, y_suction

    @property
    def file_title(self):
        """
        returns a string that represents this class
        """
        nodes1 = self.pressure_surface.nodes
        nodes2 = self.suction_surface.nodes

        node1_str = str(nodes1).replace("\n", "").replace(" ", "")
        node2_str = str(nodes2).replace("\n", "").replace(" ", "")

        return f"pressure surface: {node1_str}, suction surface: {node2_str}"

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

        open_file.write(self.file_title + "\n")

        points = np.linspace(0, 1, number_nodes)
        p_surface_points = self.pressure_surface.get_xy_coords(points)
        s_surface_points = self.suction_surface.get_xy_coords(points)[::-1]

        all_points = np.concatenate((s_surface_points, p_surface_points))

        for i in all_points:
            open_file.write(f"{i[0]} {i[1]}\n")


    def check_fits(self, shape: "TwoDimentional"):
        """
        checks that a 2D shape fits inside this aerofoil
        """
        x, y = self.suction_surface.get_xy_coords()
        boolean = True

        # check suction surface
        skip_number = 0
        for index, x_val in enumerate(x):

            try:
                y_top, _ = shape.get_y_vals(x_val)
            except:
                skip_number += 1
                continue

            if y[index] <= y_top:
                return False

        # for when the whole object is located outside of the aerofoil x range
        if len(x) == skip_number:
            return False

        # check pressure surface
        x, y = self.pressure_surface.get_xy_coords()

        for index, x_val in enumerate(x):
            try:
                _, y_bottom = shape.get_y_vals(x_val)
            except:
                continue

            if y[index] >= y_bottom:
                return False



        return boolean




class Surface():
    """
    Class that represents a Surface from a number of nodes and degree
    """

    def __init__(self, nodes, degree: int = 2):
        self.nodes = nodes
        self.degree = degree

    def get_xy_coords(self, num_points = 100):
        """
        get x and y coordinates of the whole surface
        """
        s_vals = np.linspace(0, 1, num_points)
        points = self.bezier.evaluate_multi(s_vals)
        x, y = zip(*points)

        return list(x), list(y)

    def get_y(self, x: float, **kwargs):
        """
        Get the y coordinate of a point given by x

        returns:
            y coordinate, s value
        """

        def newton_rap(function, target, **kwargs):

            def get_zero_function(function, target):

                def the_function(x):
                    coords = function(x)
                    return coords[0][0] - target

                return the_function

            return opt.newton(get_zero_function(function, target), **kwargs)

        s = newton_rap(self.bezier.evaluate, x, **kwargs)
        return self.bezier.evaluate(s)[0][1], s

    @property
    def bezier(self):
        """
        create a bezier curve class from the nodes
        """
        return bezier.Curve(self.nodes, degree = self.degree)
