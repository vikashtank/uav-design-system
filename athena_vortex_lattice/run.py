import sys
import os
sys.path.append(os.path.dirname(__file__) + "/../common")
import subprocess
import tempfile
import shutil
import time
from process import Process, Runner


class AVLRunner(Runner):

    result_aliases = {"st": "stability derivatives",
                        "ft" : "forces",
                        "hm" : "hinge moments"}


    def setup_analysis(self, geom_file, mass_file, config_file, required_files):
        self.geom_file = self._move_to_runtime(self.temp_folder, geom_file)
        self.mass_file = self._move_to_runtime(self.temp_folder, mass_file)
        self.config_file = self._move_to_runtime(self.temp_folder, config_file)
        for required_file in required_files:
            self._move_to_runtime(self.temp_folder, required_file)
        self.process = Process.initialise_process(self.executable)

        self.process.command("LOAD " + self.geom_file)
        self.process.command("MASS " + self.mass_file)
        self.process.command("MSET 0")
        self.process.command("OPER " + "f " + self.config_file)


    def generate_results(self, keep_results = True, results_dir = ""):
        """
        create a file for each result and return a dictionary with the files
        content
        """
        results_dict = {}
        self.process.command("X")

        for analysis_name in AVLRunner.result_aliases.keys():

            temp_file = analysis_name + ".txt"
            content = self._get_results(analysis_name, temp_file, keep_results)
            analysis_alias = AVLRunner.result_aliases[analysis_name]
            results_dict[analysis_alias] = content
            if os.path.exists(results_dir):
                shutil.copy(temp_file, results_dir)

        return results_dict


    def _get_results(self, analysis_name, temp_file, keep_file = True):


        command = analysis_name + " {0}".format(temp_file)
        self.process.command(command)

        while not os.path.exists(temp_file):
            time.sleep(0.1)

        with open(temp_file) as open_file:
            content = open_file.read()

        if not keep_file:
            os.remove(temp_file)

        return content


if __name__ == "__main__":
    pass
