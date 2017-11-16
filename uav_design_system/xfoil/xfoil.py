"""
Xfoil API
"""
import sys
import os
from ..common import Process, Runner
import time
import tempfile
import shutil


class XfoilRunner():
    """
    class for running xfoil through python
    """

    def __init__(self, file_path):
        """
        inputs:

            file_path (str): path to xfoil executable (located in xfoil.app/ MacOS)
        """

        # make a temp folder to run analysis in
        # temp folder located here because xfoil file path limit (64 chars)
        home_directory = os.getenv("HOME")
        self.temp_folder = os.path.join(home_directory, "temp")
        os.makedirs(self.temp_folder)

        # create a variable for the path to the location of the xfoil executable
        self.executable = file_path


    def __del__(self):
        """
        remove temporary folder with results
        """
        shutil.rmtree(self.temp_folder)


    def setup_analysis(self, aerofoil_file_path, Re):
        """
        runs commands to setup the aerofoil and reynolds number
        sets up polar plotting

        inputs:

        aerofoil (Str): naca aerofoil 4 or 5 series code
        re (Int): reynolds number
        """

        base_name = os.path.basename(aerofoil_file_path)
        shutil.copy(aerofoil_file_path, self.temp_folder)
        aerofoil_file_path = os.path.join(self.temp_folder, base_name)

        self.reynolds_number = Re
        self.process = Process.initialise_process(self.executable)
        self.process.command("LOAD {0}".format(aerofoil_file_path))
        self.process.command("OPER")
        self.process.command("visc {0}".format(self.reynolds_number))
        self.process.command("SEQP")


    def generate_results(self, start, stop, step, keep_results = True, results_dir = ""):
        """
        creates a results file and returns the results at a number of angles
        of attack of the aerofoil

        Inputs:

            start (Int): start angle of attack
            stop (Int): ending angle of attack
            step (Int): setp size
            keep_results (Bool): whether to keep all results files
            results_dir (Str): location to copy results to if kept
        """

        temp_file = os.path.join(self.temp_folder, "aerofoil_results.txt")
        self.process.command("PACC")
        self.process.command("{0}".format(temp_file))
        self.process.command("")

        content = self._get_results(start, stop, step, temp_file)

        if keep_results:
            shutil.copy(temp_file, results_dir)

        shutil.rmtree(self.temp_folder)

        return content


    def _get_results(self, start, stop, step, temp_file):
        """
        creates a results file and returns the results at a number of angles
        of attack of the aerofoil

        Inputs:

            start (Int): start angle of attack
            stop (Int): ending angle of attack
            step (Int): setp size
            temp_file (str): file path to write file to

        Returns:
            content (str): content of results in temp_file
        """

        self.process.command("ASEQ {0} {1} {2}".format(start, stop, step))

        # tune so that xfoil runs results within this time


        # check the file exists
        i = 0
        while not os.path.exists(temp_file):
            time.sleep(0.1)
            if i == 25:
                i+=1
                break

        # waiting until file has been fully written to
        start_size = os.stat(temp_file).st_size
        new_size = 0

        while start_size != new_size:
            time.sleep(0.2)
            start_size = new_size
            new_size  = os.stat(temp_file).st_size

        # read the content of the file
        with open(temp_file) as open_file:
            content = open_file.read()

        return content



if __name__ == "__main__":
    pass
