"""
class to wrap the Popen class from the subprocess library
"""
import subprocess
import os
import shutil
from pathlib import Path


class Runner():

    def __init__(self, file_path):
        """
        Creates a runtime directory and process for an executable
        inputs:

            file_path (str): path to executable
        """

        # make a temp folder to run analysis in
        # temp folder located here because xfoil file path limit (64 chars)
        home_directory = Path(os.getenv('HOME'))
        self._temp_folder = home_directory / 'temp'

        if self._temp_folder.exists():
            shutil.rmtree(str(self._temp_folder))

        os.makedirs(self._temp_folder)

        # create a variable for the path to the location of the xfoil executable
        self.executable = file_path

    @property
    def run_time_directory(self):
        return str(self._temp_folder)


    def move_to_runtime(self, file_path):
        file_path = Path(file_path)
        shutil.copy(file_path, self._temp_folder)
        return str(self._temp_folder / file_path.name )

    def __del__(self):
        shutil.rmtree(str(self._temp_folder))


class Process():

    def __init__(self, process):
        self.process = process

    def command(self, command):
        command = self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        return command

    def __del__(self):
        self.close()

    def close(self):
        self.process.stdout.close()
        self.process.stdin.close()
        self.process.kill()
        self.process.poll()

    @staticmethod
    def initialise_process(file_path: str, cwd: str = ""):

        if cwd is "":
            process = subprocess.Popen([file_path], stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            universal_newlines=True)
        else:
            process = subprocess.Popen([file_path],cwd = cwd, stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            universal_newlines=True)

        return Process(process)

    def print(self):
        self.process.stdin.close()
        i = 0
        while i < 500:
            i += 1
            print(self.process.stdout.readline())
