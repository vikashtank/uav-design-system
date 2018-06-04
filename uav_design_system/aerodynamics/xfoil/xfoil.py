"""
Xfoil API
"""
import sys
import os
from ...common import Process, Runner
import time
import tempfile
import shutil
from .results import AerofoilResults
from pathlib import Path


class XfoilRunner():
    """
    class for running xfoil through python
    """

    def __init__(self, xfoil_file_path):
        """
        inputs:

            file_path (str): path to xfoil executable (located in xfoil.app/ MacOS)
        """
        # temp folder located here because xfoil file path limit (64 chars)
        self.temp_folder = self._create_temp_folder()
        # create a variable for the path to the location of the xfoil executable
        self.executable = xfoil_file_path

    def __del__(self):
        """
        remove temporary folder with results
        """
        self._delete_temp_folder()

    def _create_temp_folder(self):
        temp_folder = Path.home() / 'xfoil_temp'
        temp_folder.mkdir()
        return temp_folder

    def _delete_temp_folder(self):
        shutil.rmtree(str(self.temp_folder))

    def _move_aerofile_to_temp(self, aerofoil_file_path):
        base_name = os.path.basename(aerofoil_file_path)
        shutil.copy(aerofoil_file_path, str(self.temp_folder))
        return self.temp_folder / base_name

    def _disable_x11_plot(self):
        self.process.command('PLOP\nG\n')

    def _prepare_aerofoil(self, aerofoil_file_path):
        aerofoil_file_path = self._move_aerofile_to_temp(aerofoil_file_path)
        self.process.command(f'LOAD {aerofoil_file_path}')

    def _setup_analysis(self, reynolds_number):
        """
        runs commands to setup the aerofoil and reynolds number
        sets up polar plotting

        inputs:

        aerofoil (Str): naca aerofoil 4 or 5 series code
        re (Int): reynolds number
        """
        self.process.command('OPER')
        self.process.command(f'visc {reynolds_number}')
        self.process.command('SEQP')

    def _prepare_output_file(self):
        temp_file = self.temp_folder / 'aerofoil_results.txt'
        self.process.command('PACC')
        self.process.command(str(temp_file))
        self.process.command('')
        return temp_file

    def _modify_geometry(self, x_location, y_location, deflection_down):
        self.process.command('GDES')
        self.process.command(f'flap {x_location} {y_location} {deflection_down}')
        self.process.command('x')
        self.process.command('')

    def __call__(self, aerofoil_file, reynolds_number, start, stop, step, results_dir = None, flap_info = None):
        """
        creates a results file and returns the results at a number of angles
        of attack of the aerofoil

        Inputs:
            aerfoil_file_path: path to aerofoil file
            reynolds_number: reynolds number of flow
            start (Int): start angle of attack
            stop (Int): ending angle of attack
            step (Int): setp size
            results_dir (Str): location to copy results to if kept, default None
        """
        self.process = Process.initialise_process(self.executable)
        self._disable_x11_plot()
        self._prepare_aerofoil(aerofoil_file)
        if flap_info: self._modify_geometry(flap_info[0],
                                                flap_info[1],
                                                flap_info[2])
        self._setup_analysis(reynolds_number) #TODO add mach number and turbulence params

        temp_file = self._prepare_output_file()

        content = self._run_analysis(start, stop, step, temp_file)

        self.process.close()

        if results_dir:
            shutil.copy(temp_file, results_dir)

        return AerofoilResults(self._format_content(content))

    def _format_content(self, content):
        """
        takes an xfoil results string and formats it into Json
        """

        def get_analysis_dict(line):
            dict = {}
            dict['alpha'] = float(line[0])
            dict['cl'] = float(line[1])
            dict['cd'] = float(line[2])
            dict['cm'] = float(line[4])
            return dict

        lines = content.split('\n')
        lines = [line.strip().split() for line in lines]
        lines = [line for line in lines if line]

        analysis_dict = {}

        parameters_dict = {}
        parameters_dict['xtrf_top'] = float(lines[3][2])
        parameters_dict['xtrf_bottom'] = float(lines[3][4])
        parameters_dict['mach'] = float(lines[4][2])
        parameters_dict['Ncrit'] = float(lines[4][-1])
        parameters_dict['reynolds_number'] = float(''.join(lines[4][5:8]))

        results_list = []
        for line in lines[7:]:
            results_list.append(get_analysis_dict(line))

        analysis_dict['results'] = results_list
        analysis_dict['name'] = ' '.join(lines[1][3:])
        analysis_dict['analysis_parameters'] = parameters_dict

        xfoil_dict = {}
        xfoil_dict['version'] = float(lines[0][2])
        xfoil_dict['analysis'] = analysis_dict

        root = {}
        root['xfoil'] = xfoil_dict

        return root

    def _run_analysis(self, start, stop, step, temp_file):
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

        self.process.command(f'ASEQ {start} {stop} {step}')

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
