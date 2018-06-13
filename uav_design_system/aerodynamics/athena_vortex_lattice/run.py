import sys
import os
sys.path.append(os.path.dirname(__file__) + "/../../common")
import subprocess
import tempfile
from typing import List
import shutil
import time
from process import Process, Runner
from .results import AVLResults


class AVLRunner(Runner):

    result_aliases = {"st" : "stability_derivatives",
                      "ft" : "total_forces",
                      "hm" : "hinge_moments",
                      "fn" : "surface_forces",
                      "fs" : "strip_forces",
                      "vm" : "structural_forces"}

    def __init__(self):
        super().__init__(os.path.join(os.path.dirname(__file__), "avl3.35"))

    def setup_analysis(self, geom_file: str, mass_file: str, config_file: str,
                       *required_files: str):
        """
        sets up AVL analysis

        Inputs:
            geom_file: geometry file path for AVL
            mass_file: mass file path for AVL
            config_file: configuration file path for AVL
            required_files: additional file paths for files used in analysis
        """
        # move files to run time directory
        self.geom_file = self._move_to_runtime(geom_file)
        self.mass_file = self._move_to_runtime(mass_file)
        self.config_file = self._move_to_runtime(config_file)
        for required_file in required_files:
            self._move_to_runtime(required_file)

        # begin avl executable
        self.process = Process.initialise_process(self.executable, cwd = self.run_time_directory)

        self.process.command("LOAD " + self.geom_file)
        self.process.command("CASE " + self.config_file)
        self.process.command("MASS " + self.mass_file)
        self.process.command("MSET 0")


    def generate_results(self, results_dir: str = ""):
        """
        create a file for each result and return a dictionary with the files
        content.
        copies content into results_dir

        Inputs:
            results_dir: path to results directory

        Returns:
            results_dict: A dictionary of analysis names and results in string
            format
        """
        results_dict = {}
        self.process.command("OPER")
        self.process.command("c1")
        self.process.command("")
        self.process.command("X")

        for analysis_name in AVLRunner.result_aliases.keys():

            temp_file = os.path.join(self.temp_folder, analysis_name + ".txt")
            content = self._get_results(analysis_name, temp_file)

            analysis_alias = AVLRunner.result_aliases[analysis_name]
            results_dict[analysis_alias] = content
            shutil.copy(temp_file, results_dir)

        return AVLResults(results_dict)


    def _get_results(self, analysis_name: str, file_name: str) -> str:
        """
        runs an analysis process and generates a temporary file

        Inputs:
            analysis_name:  The AVL command to run a certain analysis
            file_name:  The file to be created by AVL with analysis results

        Returns:
            content: The content of the file
        """
        command = analysis_name + " {0}".format(file_name)
        self.process.command(command)

        # BUG: when the print_it is performed here the values of xref and zref
        # are different to those put in output filex

        while not os.path.exists(file_name):
            time.sleep(0.1)
        with open(file_name) as open_file:
            content = open_file.read()

        return content

    def __del__(self):
        self.process.command("")
        self.process.command("quit")
        super().__del__()


if __name__ == "__main__":
    pass
